from __future__ import unicode_literals
from io import BytesIO
import datetime
import tempfile
from django.core.mail import EmailMessage
from django.core.files import File
from django.contrib import admin, messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.text import slugify, Truncator
from django.utils.translation import ugettext_lazy as _

from .models import Occupant, Document, TypeDocument
from quittance.models import Quittance
from rental.models import Rental

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration


class DocumentInline(admin.TabularInline):
    model = Document

def bulk_send_quittance(modeladmin, request, queryset):
    rentals = Rental.objects.filter(occupant__in=queryset)
    today = datetime.date.today()
    current_month = _(today.strftime('%B'))

    for rental in rentals:
        if rental.occupant.user.email:
            try:
                name = slugify(rental.occupant)
                date = today.strftime('%Y-%m-%d')
                sum_rent = rental.charges+rental.rent_amount
                occupant_email = rental.occupant.user.email
                filename = '{}-{}.pdf'.format(date, name)

                html_string = render_to_string("quittance/quittance_base.html", {
                    'rentals': rental,
                    'today': today,
                    'sum_rent': sum_rent,
                })
                html = HTML(string=html_string)
                with tempfile.TemporaryDirectory() as tmpdirname:
                    result = html.write_pdf(target='{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename))

                    quittance_to_store = open('{tmpdirname}{filename}'.format(tmpdirname=tempfile.gettempdir(), filename=filename), 'rb+')
                    # Convert it to a Django File.
                    django_file = File(quittance_to_store)
                    stored_quittance = Quittance()
                    stored_quittance.date_of_issue = today
                    saved_quittance = stored_quittance.quittance.save(filename, django_file, save=True)

                    try:
                        occupant_name = rental.occupant.user.last_name
                        occupant_firstname = rental.occupant.user.first_name
                        admin_name = rental.property.administrator.user.last_name
                        admin_firstname = rental.property.administrator.user.first_name
                        message = "Bonjour {} {}, \n Vous trouverez ci-joint la quittance de loyer pour {}. \n Cordialement, \n {} {}".format(
                            occupant_firstname, occupant_name, current_month, admin_firstname, admin_name
                        )
                        email_from = settings.EMAIL_HOST_USER
                        email = EmailMessage(
                            'Quittance de loyer', message, email_from,
                            [occupant_email],)
                        email.attach_file(stored_quittance.quittance.path)
                        email.send(fail_silently=False)
                        admin_message = "Le mail pour {} {} a bien été envoyé".format(occupant_name, occupant_firstname)
                        messages.success(request, admin_message)

                    except Occupant.DoesNotExist:
                        admin_error_message = "Le mail pour {} {} n\'a pas pu être envoyé".format(occupant_name, occupant_firstname)
                        messages.error(request, admin_error_message)

            except Occupant.DoesNotExist:
                pass
bulk_send_quittance.short_description = "Envoyer une quittance"

class OccupantModelAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_firstname', 'date_of_entry', 'date_of_leaving',
        'deposit', 'last_update', 'creation_date', 'get_suivi', 'is_active'
    ]
    list_filter = ['user__last_name', 'is_active']
    inlines = [DocumentInline,]
    actions = [bulk_send_quittance]

    def get_suivi(self, occupant):
        return Truncator(occupant.suivi).chars(40, truncate='...')
    # En-tête de notre colonne
    get_suivi.short_description = 'Aperçu du suivi'


    def get_name(self, obj):
        return obj.user.last_name
        get_name.short_description = "Name"

    def get_firstname(self, obj):
        return obj.user.first_name
        get_firstname.short_description = "First name"
    #
    # def get_doc(self, obj):
    #     return obj.doc_id.uploaded_to
    #     get_doc.short_description = "Doc"

admin.site.register(Occupant, OccupantModelAdmin)
admin.site.register(TypeDocument)
admin.site.register(Document)

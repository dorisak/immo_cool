from django.contrib import admin
from .models import Occupant, Document, TypeDocument
from django.utils.text import Truncator


class DocumentInline(admin.TabularInline):
    model = Document

class OccupantModelAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_firstname', 'date_of_entry', 'date_of_leaving',
        'deposit', 'last_update', 'creation_date', 'get_suivi', 'is_active'
    ]
    list_filter = ['user', 'is_active', 'occupant__property']
    inlines = [DocumentInline,]

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

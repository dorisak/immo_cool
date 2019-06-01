# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from rental.models import Rental
import datetime


def quittance_pdf(request):
    rentals = get_object_or_404(Rental, archived=False)
    today = datetime.date.today()
    # for rental in rentals:
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename={date}-{name}-quittance.pdf".format(
        date=today.strftime('%Y-%m-%d'),
        name=slugify(rentals.occupant.last_name),
    )
    html = render_to_string("quittance/quittance_base.html", {
        'rentals': rentals
            # 'occupant_name': rental.occupant.name,
            # 'occupant_firstname': rental.occupant.occupant.firstname,
            # 'property': rental.property.name,
            # 'property_address': rental.property.address,
            # 'bedroom': rental.bedroom.name,
            # 'rent_amount': rental.rent_amount,
            # 'date_of_issue': today,
    })

    HTML(string=html).write_pdf(response)
    return response

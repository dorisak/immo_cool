# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from rental.models import Rental
from django.shortcuts import get_object_or_404
import datetime


def quittance_pdf(request):
    """ Get data to create quittance template """
    rentals = Rental.objects.filter(archived=False).first()
    today = datetime.date.today()
    date = today.strftime('%Y-%m-%d')
    name = slugify(rentals.occupant)
    sum_rent = rentals.charges+rentals.rent_amount
    # filename = '{date}-{name}-quittance.pdf'
    filename = 'mypdf.pdf'
    response = HttpResponse(content_type="application/pdf")
    # response['Content-Disposition'] = "inline; filename={date}-{name}-quittance.pdf"
    response['Content-Disposition'] = "inline; filename=mypdf.pdf"


    html = render_to_string("quittance/quittance_base.html", {
        'rentals': rentals,
        'today': today,
        'sum_rent': sum_rent,
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

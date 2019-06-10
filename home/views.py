from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import loader
from rental.models import Rental


# TO DO: FILTRER LA VUE POUR LES ADMINS ONLY + FILTRER REQUETE SUR L'ADMIN EN LIGNE
def home(request):
    """ Get the homepage and display the information for the dashboard """
    if request.method == 'GET':
        dash = []

        for item in Rental.objects.filter(archived=False):
            details = {
                'occupant': item.occupant,
                'rent_amount': item.rent_amount,
                'charges': item.charges,
                'property': item.property,
            }
            dash.append(details)
            print(details)
            context = {'dash': dash}
        # print(item.property.administrator.user.first_name)

        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

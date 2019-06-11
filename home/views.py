from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import loader
from rental.models import Rental
from .models import Administrator


# TO DO: FILTRER LA VUE POUR LES ADMINS ONLY + FILTRER REQUETE SUR L'ADMIN EN LIGNE
def home(request):
    """ Get the homepage and display the information for the dashboard """
    if request.method == 'GET':
        dash = []
        admin_dashboard = Administrator.objects.filter(user__last_name='test')
        print(admin_dashboard, 'admin')

        # dashboard = Rental.objects.filter(archived=False, property__administrator__in=admin_dashboard)
        # print(dashboard, 'dash')
        #
        # for item in dashboard:
        #     print(item, 'item')
        #     details = {
        #         'occupant': item.occupant,
        #         'rent_amount': item.rent_amount,
        #         'charges': item.charges,
        #         'property': item.property,
        #     }
        #     dash.append(details)
        #     print(details)
        context = {'admin_dash': admin_dashboard}
        # print(item.property.administrator.user.first_name)

        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

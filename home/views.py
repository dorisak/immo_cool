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
        context = {'admin_dash': admin_dashboard}

        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

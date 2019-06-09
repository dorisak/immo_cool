from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def home(request):
    """ Get the homepage """

    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(request=request))

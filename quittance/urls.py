from django.urls import path, include
from . import views

app_name = 'quittance'

urlpatterns = [
    path('pdf', views.quittance_pdf, name='pdf'),
]

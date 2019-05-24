from django.contrib import admin
from .models import Quittance



class QuittanceAdminModel(admin.ModelAdmin):
    list_display = ['date', 'property', 'bedroom', 'occupant', 'monthly_rent_paid', 'date_of_payment']
admin.site.register(Quittance, QuittanceAdminModel)

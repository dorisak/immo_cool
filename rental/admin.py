from django.contrib import admin
from .models import Bedroom, Property, Rental


class BedroomAdminModel(admin.ModelAdmin):
    list_display = ['name', 'occupency', 'superficy']
    list_filter = ['occupency']

class PropertyAdminModel(admin.ModelAdmin):
    list_display = ['name', 'number_of_bedroom', 'superficy', 'bedroom_id', 'administrator_id']
    list_filter = ['name', 'administrator_id']

class RentalAdminModel(admin.ModelAdmin):
    list_display = ['rent_amount', 'archived']

admin.site.register(Bedroom, BedroomAdminModel)
admin.site.register(Property, PropertyAdminModel)
admin.site.register(Rental, RentalAdminModel)

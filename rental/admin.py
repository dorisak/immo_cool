from django.contrib import admin
from .models import Bedroom, Property, Rental
from quittance.models import Quittance


class QuittanceInline(admin.TabularInline):
    model = Quittance
    fields = ['quittance']

class BedroomAdminModel(admin.ModelAdmin):
    list_display = ['name', 'occupency', 'superficy']
    list_filter = ['occupency']

class PropertyAdminModel(admin.ModelAdmin):
    list_display = ['name', 'number_of_bedroom', 'superficy', 'bedroom', 'administrator']
    list_filter = ['name', 'administrator']

class RentalAdminModel(admin.ModelAdmin):
    list_display = ['name', 'rent_amount', 'bedroom', 'property', 'archived']
    # POUR AFFICHER LES QUITTANCES DE LOYER
    inlines = [QuittanceInline,]

    def name(self, obj):
        return obj.occupant_id
        name.short_description = "Name"

    def bedroom(self, obj):
        return obj.bedroom_id.name
        bedroom.short_description = "Bedroom"

    def property(self, obj):
        return obj.property_id.name
        property.short_description = "Property"

admin.site.register(Bedroom, BedroomAdminModel)
admin.site.register(Property, PropertyAdminModel)
admin.site.register(Rental, RentalAdminModel)

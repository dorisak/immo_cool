from django.contrib import admin
from .models import Bedroom, Property, Rental
from quittance.models import Quittance, Echeance


class QuittanceInline(admin.TabularInline):
    model = Quittance
    fields = ['quittance']

class EcheanceInline(admin.TabularInline):
    model = Echeance
    fields = ['echeance', 'monthly_rent_paid']

def bulk_bedroom_occupency(modeladmin, request, queryset):
    queryset.update(occupency=True)
bulk_bedroom_occupency.short_description = "Indiquer les chambres occupées"

def bulk_bedroom_empty(modeladmin, request, queryset):
    queryset.update(occupency=False)
bulk_bedroom_empty.short_description = "Indiquer les chambres libres"

class BedroomAdminModel(admin.ModelAdmin):
    list_display = ['name', 'occupency', 'superficy', 'property']
    list_filter = ['occupency', 'property']
    actions = [bulk_bedroom_occupency, bulk_bedroom_empty]

class PropertyAdminModel(admin.ModelAdmin):
    list_display = ['name', 'number_of_bedroom', 'superficy', 'administrator']
    list_filter = ['name', 'administrator']
    #INLINES POUR AFFICHER LES CHAMBRES OU PAS ?????

class RentalAdminModel(admin.ModelAdmin):
    list_display = ['name', 'rent_amount', 'bedroom', 'property', 'archived']
    list_filter = ['property', 'property__administrator']
    # POUR AFFICHER LES QUITTANCES DE LOYER
    inlines = [EcheanceInline, QuittanceInline]

    def name(self, obj):
        return obj.occupant
        name.short_description = "Name"

    def bedroom(self, obj):
        return obj.bedroom.name
        bedroom.short_description = "Bedroom"

    def property(self, obj):
        return obj.property.name
        property.short_description = "Property"

admin.site.register(Bedroom, BedroomAdminModel)
admin.site.register(Property, PropertyAdminModel)
admin.site.register(Rental, RentalAdminModel)

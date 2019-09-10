from django.contrib import admin
from .models import Quittance, Echeance


class QuittanceAdminModel(admin.ModelAdmin):
    list_display = ['rental', 'date_of_issue']
    date_hierarchy = 'date_of_issue'
    list_filter = ['rental__property__administrator', 'rental__property', 'rental__occupant']


class EcheanceAdminModel(admin.ModelAdmin):
    def bulk_rent_unpaid(modeladmin, request, queryset):
        queryset.update(monthly_rent_paid=False)
    bulk_rent_unpaid.short_description = "Indiquer les échéances non payées"

    def bulk_rent_paid(modeladmin, request, queryset):
        queryset.update(monthly_rent_paid=True)
    bulk_rent_paid.short_description = "Indiquer les échéances payées"

    list_display = ['rental', 'date_of_issue', 'monthly_rent_paid']
    date_hierarchy = 'date_of_issue'
    list_filter = ['rental__property__administrator', 'rental__property', 'rental__occupant']
    actions = [bulk_rent_unpaid, bulk_rent_paid]

admin.site.register(Quittance, QuittanceAdminModel)
admin.site.register(Echeance, EcheanceAdminModel)

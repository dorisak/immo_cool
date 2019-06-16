from django.contrib import admin
from .models import Quittance



class QuittanceAdminModel(admin.ModelAdmin):
    def bulk_rent_paid(modeladmin, request, queryset):
        queryset.update(monthly_rent_paid=True)
    bulk_rent_paid.short_description = "Indiquer les quittances payées"
    
    list_display = ['__str__', 'monthly_rent_paid', 'date_of_issue']
    date_hierarchy = 'date_of_issue'
    actions = [bulk_rent_paid]
    list_filter = ['rental__property__administrator', 'monthly_rent_paid']



admin.site.register(Quittance, QuittanceAdminModel)

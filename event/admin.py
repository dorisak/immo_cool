from django.contrib import admin
from .models import TypeEventEcheance, EventEcheance


class EventEcheanceModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'description', 'type']
    list_filter = ['type']
    search_fields = ['name']
    
admin.site.register(TypeEventEcheance)
admin.site.register(EventEcheance, EventEcheanceModelAdmin)

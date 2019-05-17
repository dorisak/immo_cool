from django.contrib import admin
from .models import Occupant, Document, TypeDocument


# class OccupantModelAdmin(admin.ModelAdmin):
#


admin.site.register(Occupant)
admin.site.register(TypeDocument)
admin.site.register(Document)

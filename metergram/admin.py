from django.contrib import admin
from .models import Meter

class MeterAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'location', 'subject', 'serial', 'created']
    raw_id_fields = ['author']
    list_filter = ['group', 'author', 'location', 'subject', 'serial', 'created']
    search_fields = ['group', 'author', 'location', 'subject', 'serial', 'created']
    ordering = ['-group', '-author', 'location', '-subject', '-serial', '-created']

admin.site.register(Meter, MeterAdmin)
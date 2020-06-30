from django.contrib import admin
from .models import Meter

class MeterAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'dong', 'ho', 'mtr', 'cor', 'elec', 'water', 'created', 'action', 'charge']
    #raw_id_fields = ['id']      #
    list_filter = ['dong', 'charge', 'action']
    search_fields = ['dong', 'charge', 'created']
    ordering = ['-created', '-dong', '-ho']

admin.site.register(Meter, MeterAdmin)
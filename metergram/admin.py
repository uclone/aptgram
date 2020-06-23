from django.contrib import admin
from .models import Meter

class MeterAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'dong', 'ho', 'utility', 'serial', 'mtr', 'cor', 'created', 'action']
    #raw_id_fields = ['id']      #
    list_filter = ['dong', 'utility', 'action']
    search_fields = ['serial', 'charge', 'created']
    ordering = ['-created', '-dong', '-ho']

admin.site.register(Meter, MeterAdmin)
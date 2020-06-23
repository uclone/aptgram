from django.contrib import admin
from .models import Equip

class EquipAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'group_id', 'author', 'subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date']
    raw_id_fields = ['author']
    list_filter = ['author', 'subject', 'department', 'manager_1']
    search_fields = ['author', 'subject', 'manager_1']
    ordering = ['-author', '-subject', '-location']

admin.site.register(Equip, EquipAdmin)

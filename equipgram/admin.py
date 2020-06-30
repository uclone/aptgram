from django.contrib import admin
from .models import Equip

class EquipAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'code', 'subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date']
    raw_id_fields = ['author']
    list_filter = ['author', 'code', 'subject', 'department', 'manager_1']
    search_fields = ['author', 'code', 'subject', 'manager_1']
    ordering = ['-author', '-code', '-subject', '-location']

admin.site.register(Equip, EquipAdmin)

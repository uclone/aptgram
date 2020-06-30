from django.contrib import admin
from .models import Sulbi

class SulbiAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'department', 'code', 'subject', 'action', 'cycle', 'start', 'close']
    raw_id_fields = ['author']
    list_filter = ['code', 'subject', 'department', 'cycle', 'action']
    search_fields = ['start', 'close', 'subject', 'cycle']
    ordering = ['-code', '-subject', '-start', '-close']

admin.site.register(Sulbi, SulbiAdmin)

from django.contrib import admin
from .models import Sulbi

class SulbiAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'department', 'subject', 'action', 'start', 'close', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['subject', 'author', 'department', 'action']
    search_fields = ['start', 'close', 'subject']
    ordering = ['-updated', '-created', '-start', '-close']

admin.site.register(Sulbi, SulbiAdmin)

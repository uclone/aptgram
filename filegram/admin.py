from django.contrib import admin
from .models import File, Sfile

class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'department', 'subject', 'approval', 'charge', 'manager', 'created']
    raw_id_fields = ['author']
    list_filter = ['department', 'subject', 'approval', 'charge', 'manager']
    search_fields = ['author', 'subject', 'approval', 'charge', 'manager']
    ordering = ['approval', 'charge', '-created']

admin.site.register(File, FileAdmin)


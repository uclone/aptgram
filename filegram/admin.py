from django.contrib import admin
from .models import File, Sfile

class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'department', 'charge', 'manager', 'director', 'subject', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['department', 'charge', 'manager']
    search_fields = ['author', 'subject', 'director']
    ordering = ['-updated', '-created']

admin.site.register(File, FileAdmin)


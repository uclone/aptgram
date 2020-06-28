from django.contrib import admin
from .models import Paper

class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'subject', 'description', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['author', 'group', 'subject']
    search_fields = ['author', 'group', 'subject']
    ordering = ['-updated', '-created', '-subject']

admin.site.register(Paper, PaperAdmin)

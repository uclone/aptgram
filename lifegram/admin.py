from django.contrib import admin
from .models import Life

class LifeAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'created', 'subject', 'charge', 'updated', 'department']
    raw_id_fields = ['author']
    list_filter = ['created', 'updated', 'author']
    search_fields = ['author', 'charge', 'department']
    ordering = ['-updated', '-created']

admin.site.register(Life, LifeAdmin)
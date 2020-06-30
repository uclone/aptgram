from django.contrib import admin
from .models import Life

class LifeAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'contact', 'created', 'subject', 'department', 'charge', 'date', 'close']
    raw_id_fields = ['author']
    list_filter = ['author', 'created', 'subject',]
    search_fields = ['author', 'subject', 'charge', 'department']
    ordering = ['-created', '-date',]

admin.site.register(Life, LifeAdmin)
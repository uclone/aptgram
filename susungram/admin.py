from django.contrib import admin
from .models import Susun

class SusunAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'category', 'subject', 'cycle', 'last', 'rule', 'plan', 'cost']
    raw_id_fields = ['author']
    list_filter = ['category', 'subject', 'cycle', 'last', 'rule']
    search_fields = ['category', 'subject', 'cycle', 'last', 'rule']
    ordering = ['-category', '-subject', '-cycle', '-last', '-rule']

admin.site.register(Susun, SusunAdmin)

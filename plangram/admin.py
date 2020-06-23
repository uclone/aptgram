from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'start', 'close', 'department', 'charge', 'subject', 'manager', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['start', 'close', 'department', 'charge', 'manager']
    search_fields = ['subject', 'author', 'manager', 'director']
    ordering = ['-updated', '-created', '-start', '-close']

admin.site.register(Plan, PlanAdmin)

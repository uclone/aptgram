from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'department', 'subject', 'remark', 'updated']
    raw_id_fields = ['author']
    list_filter = ['group', 'department', 'author', 'updated']
    search_fields = ['group', 'department', 'author', 'updated']
    ordering = ['-group', '-department', '-updated']

admin.site.register(Plan, PlanAdmin)

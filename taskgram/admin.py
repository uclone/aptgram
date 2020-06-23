from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'department', 'charge', 'created', 'subject', 'manager']
    raw_id_fields = ['author']
    list_filter = ['created', 'department', 'author', 'subject']
    search_fields = ['author', 'department', 'created']
    ordering = ['-created', '-department']

admin.site.register(Task, TaskAdmin)

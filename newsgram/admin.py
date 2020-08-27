from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'group', 'dong', 'ho', 'date', 'subject', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['dong', 'ho']
    search_fields = ['dong', 'ho', 'date', 'subject']
    ordering = ['-date', '-updated']

admin.site.register(News, NewsAdmin)

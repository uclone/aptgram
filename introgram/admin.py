from django.contrib import admin
from .models import Intro

class IntroAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'group', 'name', 'metro', 'city', 'address', 'remark']
    raw_id_fields = ['author']
    list_filter = ['metro', 'city', 'name']
    search_fields = ['metro', 'city', 'name']
    ordering = ['-metro', '-city', 'name']

admin.site.register(Intro, IntroAdmin)

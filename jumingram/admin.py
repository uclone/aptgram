from django.contrib import admin
from .models import Jumin

class JuminAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'created', 'updated']
    raw_id_fields = ['author']
    list_filter = ['dong']
    search_fields = ['dong', 'ho', 'represent', 'car']
    ordering = ['-updated', '-created']

admin.site.register(Jumin, JuminAdmin)

from django.contrib import admin
from .models import Poll, Choice, Spoll

class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'author', 'subject', 'pub_date', 'remark', 'open_date', 'close_date']
    raw_id_fields = ['author']
    list_filter = ['group', 'subject', 'author', 'pub_date']
    search_fields = ['group', 'subject', 'author', 'pub_date']
    ordering = ['-group', '-subject', '-pub_date']

admin.site.register(Poll, PollAdmin)
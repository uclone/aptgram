from django.contrib import admin
from .models import Resident

class ResidentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['dong']}),
        (None,          {'fields': ['ho']}),
        (None,          {'fields': ['represent']}),
        (None,          {'fields': ['family']}),
        (None,          {'fields': ['phone']}),
        (None,          {'fields': ['date']}),
        (None,          {'fields': ['car']}),
        (None,          {'fields': ['remark']}),
    ]

    list_display = ( 'dong', 'ho', 'represent', 'family', 'phone', 'date', 'car', 'remark')
    list_filter = ['dong']
    search_fields = ['represent', 'family', 'car']

admin.site.register(Resident, ResidentAdmin)
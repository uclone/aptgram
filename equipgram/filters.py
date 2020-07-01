from django.contrib.auth.models import User
from .models import Equip
from .views import *
from django import forms
import django_filters
from bootstrap_datepicker_plus import DatePickerInput

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Equip
        fields = {
            'code': ['icontains'],
            'subject': ['icontains'],
            'location': ['icontains'],
            'date': ['range'],
        }

#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#            'date': ['date_month_year__gt', 'date_month_year__lt'],
#        }


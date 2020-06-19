from django.contrib.auth.models import User
from .models import Plan
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = {
            'department': ['icontains'],
            'subject': ['icontains'],
            'start': ['year__lt', 'year__gt'],
            'close': ['year__lt', 'year__gt'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
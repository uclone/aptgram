from django.contrib.auth.models import User
from .models import Plan
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = {
            'department': ['icontains'],
            'charge': ['icontains'],
            'subject': ['icontains'],
            'start': ['range'],
            'close': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
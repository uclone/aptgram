from django.contrib.auth.models import User
from .models import Life
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Life
        fields = {
            'subject': ['icontains'],
            'contact': ['icontains'],
            'department': ['icontains'],
            'charge': ['icontains'],
            'created': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
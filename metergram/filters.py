from django.contrib.auth.models import User
from .models import Meter
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Meter
        fields = {
            'dong': ['icontains'],
            'ho': ['icontains'],
            'action': ['icontains'],
            'charge': ['icontains'],
            'manager': ['icontains'],
            'created': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
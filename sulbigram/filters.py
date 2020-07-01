from django.contrib.auth.models import User
from .models import Sulbi
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Sulbi
        fields = {
            'subject': ['icontains'],
            'code': ['icontains'],
            'action': ['icontains'],
            'cycle': ['icontains'],
            'start': ['range'],
            'close': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
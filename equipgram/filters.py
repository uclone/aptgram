from django.contrib.auth.models import User
from .models import Equip
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Equip
        fields = {
            'subject': ['icontains'],
            'location': ['icontains'],
            'date': ['year__gt', 'year__lt'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
from django.contrib.auth.models import User
from .models import Jumin
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Jumin
        fields = {
            'dong': ['icontains'],
            'ho': ['icontains'],
            'represent': ['icontains'],
            'family': ['icontains'],
            'car': ['icontains'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
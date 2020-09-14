from django.contrib.auth.models import User
from .models import Intro
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Intro
        fields = {
            'metro': ['icontains'],
            'city': ['icontains'],
            'address': ['icontains'],
            'name': ['icontains'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }

class IntroFilter(django_filters.FilterSet):
    class Meta:
        model = Intro
        fields = {
            'metro': ['icontains'],
            'city': ['icontains'],
            'address': ['icontains'],
            'name': ['icontains'],
        }
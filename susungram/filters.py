from django.contrib.auth.models import User
from .models import Susun
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Susun
        fields = {
            'category': ['icontains'],
            'subject': ['icontains'],
            'treatment': ['icontains'],
            'cycle': ['icontains'],
            'last': ['range'],
            'rule': ['range'],
        }
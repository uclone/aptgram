from django.contrib.auth.models import User
from .models import Shrimp
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Shrimp
        fields = {
            'location': ['icontains'],
            'subject': ['exact'],
            'serial': ['exact'],
            'date': ['range'],
        }
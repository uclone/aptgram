from django.contrib.auth.models import User
from .models import Meter
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Meter
        fields = {
            'location': ['icontains'],
            'subject': ['exact'],
            'serial': ['exact'],
            'created': ['range'],
        }

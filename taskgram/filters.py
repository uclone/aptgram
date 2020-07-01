from django.contrib.auth.models import User
from .models import Task
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'department': ['icontains'],
            'charge': ['icontains'],
            'subject': ['icontains'],
            'created': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
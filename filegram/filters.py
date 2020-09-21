from django.contrib.auth.models import User
from .models import File
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = File
        fields = {
            'subject': ['icontains'],
            'department': ['icontains'],
            'approval': ['icontains'],
            'created': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
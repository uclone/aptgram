from django.contrib.auth.models import User
from .models import News
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = {
            'dong': ['exact'],
            'ho': ['exact'],
            'date': ['range'],
            'subject': ['icontains'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }

class GongoFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = {
            'dong': ['exact'],
            'ho': ['exact'],
            'date': ['range'],
            'subject': ['icontains'],
        }
from django.contrib.auth.models import User
from .models import Poll
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Poll
        fields = {
            'subject': ['icontains'],
            'pub_date': ['range'],
            'open_date': ['range'],
            'close_date': ['range'],
        }
#        fields = {
#            'price': ['lt', 'gt'],
#            'release_date': ['exact', 'year__gt'],
#        }
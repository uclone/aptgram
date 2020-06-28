from django.contrib.auth.models import User
from .models import Paper
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Paper
        fields = {
            'subject': ['icontains'],
            'description': ['icontains'],
        }

from django.contrib.auth.models import User
from .models import Plan
from .views import *
import django_filters

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = {
            'regpsw': ['icontains'],
            'updated': ['range'],
        }

from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import Resident

app_name = 'resident'

urlpatterns = [
    path('', ResidentListView.as_view(), name='resident_list'),
    path('add/', ResidentCreateView.as_view(), name='resident_add'),
    path('update/<int:pk>/', ResidentUpdateView.as_view(), name='resident_update'),
    path('delete/<int:pk>/', ResidentDeleteView.as_view(), name='resident_delete'),
    path('detail/<int:pk>/', ResidentDetailView.as_view(), name='resident_detail'),
]
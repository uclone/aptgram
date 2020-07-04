from django.urls import path
from django.contrib.auth import views as auth_view
from .views import *

app_name = 'index'

urlpatterns = [
    path('', index_view, name='index'),
    path('mobile/', index_mobile_view, name='mobile'),
]
from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import KospiPredict
from . import views

app_name = 'nameapp'

urlpatterns = [
    path('', name_list, name='name_list'),
    path('upload/', NameUploadView.as_view(), name='meter_upload'),

    path('api/predict/', views.KospiPredictAPIView.as_view(), name="predict_kospi_api"),
    path('chart', views.ChartView.as_view(), name="chart"),
]

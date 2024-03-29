from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Meter, Smeter
from metergram import views
from . import *

app_name = 'metergram'

urlpatterns = [
    path('mindex/', MeterDataView.as_view(), name='mindex'),
    path('vindex/', ValveDataView.as_view(), name='vindex'),
    path('vclose/', ValveCloseView.as_view(), name='valve_close'),

    path('', meter_list, name='meter_list'),
    path('control/', control_list, name='control_list'),
    path('instrument/', instrument_list, name='instrument_list'),

    path('upload/', MeterUploadView.as_view(), name='meter_upload'),
    path('update/<int:pk>/', MeterUpdateView.as_view(), name='meter_update'),

    path('data_delete/<int:pk>/', data_delete, name='data_delete'),
    path('instrument_delete/<int:pk>/', instrument_delete, name='instrument_delete'),

    path('detail/<int:pk>/', DetailView.as_view(model=Meter, template_name='metergram/meter_detail.html'),
         name='meter_detail'),
    path('instrument_detail/<int:pk>/', DetailView.as_view(model=Meter, template_name='metergram/instrument_detail.html'),
         name='instrument_detail'),

    url(r'^search/$', meter_search, name='meter_search'),                               # search
    url(r'^control_search/$', control_search, name='control_search'),                   # search

    path('makepdf/', generate_pdf, name='generate_pdf'),                                # weasyprint
    path('controlpdf/', control_pdf, name='control_pdf'),                               # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^control_searchpdf/$', control_search_pdf, name='control_search_pdf'),

    url(r'^searchxls/$', search_xls, name='search_xls'),

    path('meter_api/<int:idd>', views.MeterAPIView.as_view(), name="meter_api"),
    path('meter_chart/', views.MeterChartView.as_view(), name="meter_chart"),
]




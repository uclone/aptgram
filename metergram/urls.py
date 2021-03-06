from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Meter, Smeter

app_name = 'metergram'

urlpatterns = [
    path('', meter_list, name='meter_list'),
    path('upload/', MeterUploadView.as_view(), name='meter_upload'),
    path('delete/<int:pk>/', MeterDeleteView.as_view(), name='meter_delete'),
    path('update/<int:pk>/', MeterUpdateView.as_view(), name='meter_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Meter, template_name='metergram/meter_detail.html'), name='meter_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                    # weasyprint
    path('detailpdf/<int:kk>', detail_pdf, name='detail_pdf'),              # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', meter_search, name='meter_search'),                   # search

    url(r'^meterpost/$', meter_post, name='meter_post'),                    #post == meter only
]
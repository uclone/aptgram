from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Susun, Ssusun

app_name = 'susungram'

urlpatterns = [
    path('', susun_list, name='susun_list'),
    path('upload/', SusunUploadView.as_view(), name='susun_upload'),
    path('delete/<int:pk>/', SusunDeleteView.as_view(), name='susun_delete'),
    path('update/<int:pk>/', SusunUpdateView.as_view(), name='susun_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Susun, template_name='susungram/susun_detail.html'), name='susun_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
    path('detailpdf/<int:kk>', detail_pdf, name='detail_pdf'),  # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', susun_search, name='susun_search'),  # search

    url(r'^searchxls/$', search_xls, name='search_xls'),
]
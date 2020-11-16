from django.urls import path
from django.views.generic.detail import DetailView
from shrimpgram.views import *
from django.conf.urls import url
from .models import Shrimp, Sshrimp
from . import views

app_name = 'shrimpgram'

urlpatterns = [
    path('sindex', views.IndexView.as_view(), name='sindex'),

    path('', shrimp_list, name='shrimp_list'),
    path('control/', control_list, name='control_list'),

    path('upload/', ShrimpUploadView.as_view(), name='shrimp_upload'),
    path('control_upload/', ControlUploadView.as_view(), name='control_upload'),

    path('delete/<int:pk>/', ShrimpDeleteView.as_view(), name='shrimp_delete'),
    path('update/<int:pk>/', ShrimpUpdateView.as_view(), name='shrimp_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Shrimp, template_name='shrimpgram/shrimp_detail.html'), name='shrimp_detail'),

    url(r'^search/$', shrimp_search, name='shrimp_search'),                             # search
    url(r'^control_search/$', control_search, name='control_search'),                   # search

    path('makepdf/', generate_pdf, name='generate_pdf'),                                # weasyprint
    path('controlpdf/', control_pdf, name='control_pdf'),                               # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^control_searchpdf/$', control_search_pdf, name='control_search_pdf'),

    url(r'^searchxls/$', search_xls, name='search_xls'),                                #excell

    path('shrimp_api/<int:idd>', views.ShrimpAPIView.as_view(), name="shrimp_api"),
    path('shrimp_chart/', views.ChartView.as_view(), name="shrimp_chart"),
]
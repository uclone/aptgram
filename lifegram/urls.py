from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Life, Slife

app_name = 'lifegram'

urlpatterns = [
    path('', life_list, name='life_list'),
    path('upload/', LifeUploadView.as_view(), name='life_upload'),
    path('delete/<int:pk>/', LifeDeleteView.as_view(), name='life_delete'),
    path('update/<int:pk>/', LifeUpdateView.as_view(), name='life_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Life, template_name='lifegram/life_detail.html'), name='life_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                                # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),                          # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', life_search, name='life_search'),                                 # search

    path('listjumin/', life_list_jumin, name='life_list_jumin'),
    url(r'^uploadjumin/$', life_upload_jumin, name='life_upload_jumin'),                                   # mobile
    path('detailjumin/<int:pk>/', life_detail_jumin, name='life_detail_jumin'),      # mobile
]
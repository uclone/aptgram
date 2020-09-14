from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Intro, Sintro

app_name = 'introgram'

urlpatterns = [
    path('', intro_list, name='intro_list'),
    path('upload/', IntroUploadView.as_view(), name='intro_upload'),
    path('delete/<int:pk>/', IntroDeleteView.as_view(), name='intro_delete'),
    path('update/<int:pk>/', IntroUpdateView.as_view(), name='intro_update'),
    path('photoupdate/<int:pk>/', PhotoUpdateView.as_view(), name='photo_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Intro, template_name='introgram/intro_detail.html'), name='intro_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                                # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),                          # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', intro_search, name='intro_search'),                               # search

    path('detailjummin/<int:pk>', intro_detail_jumin, name='intro_detail_jumin'),       # mobile
    path('listjumin/', intro_list_jumin, name='intro_list_jumin'),
]
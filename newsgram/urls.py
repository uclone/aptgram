from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import News, Snews

app_name = 'newsgram'

urlpatterns = [
    path('', news_list, name='news_list'),
    path('upload/', NewsUploadView.as_view(), name='news_upload'),
    path('delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
    path('update/<int:pk>/', NewsUpdateView.as_view(), name='news_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=News, template_name='newsgram/news_detail.html'), name='news_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),  # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', news_search, name='news_search'),  # search

    path('detailjummin/<int:pk>', news_detail_jumin, name='news_detail_jumin'),  # mobile
    path('listjumin/', news_list_jumin, name='news_list_jumin'),
]
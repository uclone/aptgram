from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Poll, Choice, Spoll

app_name = 'pollgram'

urlpatterns = [
    path('', poll_list, name='poll_list'),
    path('upload/', poll_upload, name='poll_upload'),
    path('detail/<int:pk>', poll_detail, name='poll_detail'),
    path('delete/<int:pk>/', PollDeleteView.as_view(), name='poll_delete'),
    #path('update/<int:pk>/', PollUpdateView.as_view(), name='poll_update'),
    path('update/<int:pk>', poll_update, name='poll_update'),

    path('vote/<int:pk>', poll_vote, name='poll_vote'),
    #path('result/<int:pk>', poll_result, name='poll_result'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                #weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),          #weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', poll_search, name='poll_search'),                 # search
]
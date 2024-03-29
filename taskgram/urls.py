from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Task, Stask

app_name = 'taskgram'

urlpatterns = [
    path('', task_list, name='task_list'),
    path('upload/', TaskUploadView.as_view(), name='task_upload'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Task, template_name='taskgram/task_detail.html'), name='task_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                                # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),                          # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', task_search, name='task_search'),                                 # search

    path('mobile/', task_list_mobile, name='task_list_mobile'),
    url(r'^uploadmobile/$', task_upload_mobile, name='task_upload_mobile'),                                   # mobile
    path('detailmobile/<int:pk>/', task_detail_mobile, name='task_detail_mobile'),      # mobile
]
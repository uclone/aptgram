from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Paper, Spaper

app_name = 'papergram'

urlpatterns = [
    path('', paper_list, name='paper_list'),
    path('upload/', PaperUploadView.as_view(), name='paper_upload'),
    path('delete/<int:pk>/', PaperDeleteView.as_view(), name='paper_delete'),
    path('update/<int:pk>/', PaperUpdateView.as_view(), name='paper_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Paper, template_name='papergram/paper_detail.html'), name='paper_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                    # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),              # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', paper_search, name='paper_search'),                   # search
]

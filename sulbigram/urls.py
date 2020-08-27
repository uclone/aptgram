from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Sulbi, Ssulbi

app_name = 'sulbigram'

urlpatterns = [
    path('', sulbi_list, name='sulbi_list'),
    path('upload/', SulbiUploadView.as_view(), name='sulbi_upload'),
    path('delete/<int:pk>/', SulbiDeleteView.as_view(), name='sulbi_delete'),
    path('update/<int:pk>/', SulbiUpdateView.as_view(), name='sulbi_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Sulbi, template_name='sulbigram/sulbi_detail.html'), name='sulbi_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),  # weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', sulbi_search, name='sulbi_search'),  # search
]
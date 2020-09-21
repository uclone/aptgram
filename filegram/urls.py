from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import File, Sfile

app_name = 'filegram'

urlpatterns = [
    path('', file_list, name='file_list'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
    #path('update/<int:pk>/', FileUpdateView.as_view(), name='file_update'),
    path('approval/<int:pk>/', file_approval, name='file_approval'),
    path('detail/<int:pk>/', DetailView.as_view(model=File, template_name='filegram/file_detail.html'), name='file_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),  # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', file_search, name='file_search'),  # search
]
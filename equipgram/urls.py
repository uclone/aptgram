from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Equip, Sequip

app_name = 'equipgram'

urlpatterns = [
    path('', equip_list, name='equip_list'),
    path('upload/', EquipUploadView.as_view(), name='equip_upload'),
    path('delete/<int:pk>/', EquipDeleteView.as_view(), name='equip_delete'),
    path('update/<int:pk>/', EquipUpdateView.as_view(), name='equip_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Equip, template_name='equipgram/equip_detail.html'), name='equip_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),                #weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),          #weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', equip_search, name='equip_search'),               #search
]
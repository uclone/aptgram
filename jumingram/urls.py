from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Jumin, Sjumin

app_name = 'jumingram'

urlpatterns = [
    path('', jumin_list, name='jumin_list'),
    path('date/', jumin_list_date, name='jumin_list_date'),
    path('upload/', JuminUploadView.as_view(), name='jumin_upload'),
    path('delete/<int:pk>/', JuminDeleteView.as_view(), name='jumin_delete'),
    path('update/<int:pk>/', JuminUpdateView.as_view(), name='jumin_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Jumin, template_name='jumingram/jumin_detail.html'), name='jumin_detail'),

    path('ticket', jumin_ticket, name='jumin_ticket'),
    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
    path('detailpdf/<int:pk>', detail_pdf, name='detail_pdf'),  # weasyprint ####New

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', jumin_search, name='jumin_search'),  # search

    #path('detailmobile/', jumin_detail_mobile, name='jumin_detail_mobile'),  # mobile
    #path('gongoupdate/<int:pk>/', GongoUpdateView.as_view(), name='gongo_update'),
    #path('gongocast/', gongo_cast, name='gongo_cast'),
]
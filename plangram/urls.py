from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from django.conf.urls import url
from .models import Plan, Splan

app_name = 'plangram'

urlpatterns = [
    path('', plan_list, name='plan_list'),
    path('upload/', PlanUploadView.as_view(), name='plan_upload'),
    path('delete/<int:pk>/', PlanDeleteView.as_view(), name='plan_delete'),
    path('update/<int:pk>/', PlanUpdateView.as_view(), name='plan_update'),
    path('detail/<int:pk>/', DetailView.as_view(model=Plan, template_name='plangram/plan_detail.html'), name='plan_detail'),

    path('makepdf/', generate_pdf, name='generate_pdf'),          #weasyprint
    path('detailpdf/<int:kk>', detail_pdf, name='detail_pdf'),          #weasyprint

    url(r'^searchpdf/$', search_pdf, name='search_pdf'),
    url(r'^search/$', plan_search, name='plan_search'),  # search
]
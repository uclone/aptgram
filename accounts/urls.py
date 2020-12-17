from django.urls import path
from django.contrib.auth import views as auth_view
from django.views.generic.detail import DetailView
from django.conf.urls import url
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('register_btn/', RegisterBtnView.as_view(), name='register_btn'),
    path('register/', register, name='register'),

    path('list/', account_list, name='account_list'),
    path('read/', account_read, name='account_read'),
    path('detail/<int:pk>/', DetailView.as_view(model=User, template_name='accounts/account_detail.html'), name='account_detail'),
    path('update/<int:pk>/', AccountUpdateView.as_view(), name='account_update'),
    path('delete/<int:pk>/', AccountDeleteView.as_view(), name='account_delete'),

    path('makepdf/', generate_pdf, name='generate_pdf'),  # weasyprint
]


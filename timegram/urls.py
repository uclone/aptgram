from django.conf.urls import url
from django.urls import path
from .views import *
from . import views

app_name = 'timegram'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^schedule/$', views.CalendarView.as_view(), name='schedule'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

    #url(r'^delete/(?P<pk>\d+)/$', views.delete, name='time_delete'),
    #path('delete/<int:pk>/', views.delete, name='time_delete'),
]


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

    #url(r'^event/list/(?P<pk>\d+)/$', views.event_list, name='event_list'),
    #url(r'^event/list/(?P<day>\d+)/$', views.event_list, name='event_list'),
    #path('event/list/', event_list, name='event_list'),
    #path('event/list/<int:kk>', event_list, name='event_list'),
    #path('delete/<int:pk>/', views.delete, name='time_delete'),
]


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

    #path('event/list/', event_list, name='event_list'),
    path('schedule2/<int:kk>', views.XalendarView.as_view(), name='schedule2'),
    #path('delete/<int:pk>/', views.delete, name='time_delete'),
]


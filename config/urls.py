"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static                                          #transfered to Amazon
from django.conf import settings                                                    #transfered to Amazon

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('filegram/', include('filegram.urls')),
    path('jumingram/', include('jumingram.urls')),
    path('sulbigram/', include('sulbigram.urls')),
    path('taskgram/', include('taskgram.urls')),
    path('resident/', include('resident.urls')),
    path('equipgram/', include('equipgram.urls')),
    path('plangram/', include('plangram.urls')),
    path('lifegram/', include('lifegram.urls')),
    path('index/', include('index.urls')),
    path('metergram/', include('metergram.urls')),
    path('papergram/', include('papergram.urls')),
    path('susungram/', include('susungram.urls')),
    path('timegram/', include('timegram.urls')),
    path('newsgram/', include('newsgram.urls')),
    path('introgram/', include('introgram.urls')),
    path('pollgram/', include('pollgram.urls')),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        #transfered to Amazon

"""sheetoutputbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from sheetoutput import views
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^oath2callback$', views.auth_return, name='callback'),
    re_path(r'^auth', views.authorize, name='authorize'),
    re_path(r'^refresh', views.refresh_token, name='authorize'),
    re_path(r'touch', views.touch, name='touch'),
    re_path(r'^check', views.check_token, name='authorize')
]

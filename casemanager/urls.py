"""BEE URL Configuration

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
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import home, new_case, delete_case_request_vw, new_batch, usageStats, delete_batch_request_vw, \
    new_custom_batch, delete_custom_batch_request_vw
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('home/', home, name='casemanager_home'),
    url(r'delete_case_request/(?P<id>\d+)/$', delete_case_request_vw, name='casemanager_delete_request'),
    url(r'delete_batch_request/(?P<id>\d+)/$', delete_batch_request_vw, name='casemanager_delete_batch_request'),
    url(r'delete_custom_batch_request/(?P<id>\d+)/$', delete_custom_batch_request_vw, name='casemanager_delete_custom_batch_request'),
    path('login/', LoginView.as_view(template_name='casemanager/login_form.html'), name='casemanager_login'),
    path('logout/', LogoutView.as_view(), name='casemanager_logout'),
    path('new_case/', new_case, name='casemanager_new_case'),
    path('new_batch/', new_batch, name='casemanager_new_batch'),
    path('new_custom_batch/', new_custom_batch, name='casemanager_new_custom_batch'),
    path('stats/', usageStats, name='casemanager_stats'),
]


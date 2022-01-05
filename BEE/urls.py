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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls '))
"""
from django.conf.urls import url
from django.contrib import admin
# from django.contrib.urls import url
from django.urls import path, include#, url
from caseapplication import views
from .views import *
from caseapplication.api_views import CaseList, CaseCreate, CaseDestroy, CaseRetrieveUpdateDestroy, BatchList, \
    BatchCreate, BatchRetrieveUpdateDestroy, CustomBatchList, CustomBatchCreate, CustomBatchRetrieveUpdateDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cases', CaseList.as_view()),
    path('api/v1/batch', BatchList.as_view()),
    path('api/v1/batch/<int:id>', BatchRetrieveUpdateDestroy.as_view()),
    path('api/v1/batch/new', BatchCreate.as_view()),
    path('api/v1/cases/new', CaseCreate.as_view()),
    path('api/v1/cases/<int:id>/destroy', CaseDestroy.as_view()),
    path('api/v1/cases/<int:id>', CaseRetrieveUpdateDestroy.as_view()),
    path('api/v1/custombatch/new', CustomBatchCreate.as_view()),
    path('api/v1/custombatch', CustomBatchList.as_view()),
    path('api/v1/custombatch/<int:id>', CustomBatchRetrieveUpdateDestroy.as_view()),
    # url(r'^api-auth/', include('rest_framework.urls')),
    path('', views.home, name='caseapplication_welcome'),
    path('casemanager/', include('casemanager.urls')),
    url(r'^signup/$', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]

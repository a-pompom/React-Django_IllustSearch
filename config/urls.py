"""config URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

API_VERSION = 1

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/v{API_VERSION}/login/', include('app_login.urls')),
    path(f'api/v{API_VERSION}/illust/', include('app_illust_list.urls')),
]

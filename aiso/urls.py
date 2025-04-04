"""
URL configuration for aiso project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework import routers

from mainapp.views import OrganizationViewSet, CertificateViewSet, UserViewSet, PreviewViewSet, TestView

router = routers.DefaultRouter()
router.register('service/available/organizations', OrganizationViewSet)
router.register('certificates', CertificateViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('preview/', PreviewViewSet.as_view(), name='preview'),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('test/<int:id>/', TestView.as_view(), name='test'),
] + router.urls

"""fileUpload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^imageupload/$', views.upload_image, name="upload_image"),
    url(r'^imageuploadwithmodel', views.upload_image_with_model,
        name="upload_image_with_model"),
    url(r'^imageuploadtominio/$', views.upload_image_to_minio,
        name="upload_image_to_minio"),
    url(r'^imageuploadtominiodirectly', views.upload_image_to_minio_directly,
        name="upload_image_to_minio_directly"),
    url(r'^imageuploadtominiopackage', views.upload_image_to_minio_package,
        name="upload_image_to_minio_package"),
]

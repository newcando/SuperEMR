"""SuperEMR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib import admin
from emr import urls
from emr import Ajaxurls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
from SuperEMR import settings
from emr import restfulUrls

urlpatterns = [
    url(r'^api/', include(restfulUrls.router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(urls)),#前台
    url(r'^emr/', include(urls)),#前台
    url(r'^Ajax/', include(Ajaxurls)),#前台Ajax
    url(r'^captcha/', include('captcha.urls')),#验证码
    url(r'^api/docs/', include('rest_framework_docs.urls')),
]
urlpatterns += staticfiles_urlpatterns()#静态文件
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from collector import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^detail/(?P<count>\d+)$', views.index),
    url(r'^img$', views.img),
    url(r'^put$', views.put),
)

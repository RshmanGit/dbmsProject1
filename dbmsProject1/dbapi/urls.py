from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/', views.home),
    url(r'^home/', views.rethome),
    url(r'^subscription/', views.subspage),
    url(r'^mychannels/', views.channelpage),
    url(r'^create-channel/', views.createchannel),
    url(r'^upload-video/',views.uploadvideo),
    url(r'^channel/(?P<channelId>[0-9]+)/$', views.channeldesc),
    url(r'^subscribe/(?P<channelId>[0-9]+)/$', views.subscribe),
    url(r'^register/', views.register),
    url(r'^register/registercomplete/', views.register_complete)
]

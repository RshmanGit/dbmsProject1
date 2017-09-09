from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/', views.home),
    url(r'^home/', views.rethome),
    url(r'^subscription/', views.subspage),
    url(r'^mychannels/', views.channelpage)
]

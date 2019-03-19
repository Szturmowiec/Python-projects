from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'polls'
urlpatterns=[
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('vote/', views.vote, name='vote'),
]
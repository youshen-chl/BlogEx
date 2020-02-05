
# from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'storm'

urlpatterns = [
    path('', views.hello, name='hello'),
    path('list/', views.showlist, name='showlist'),
    path('nav/', views.shownav, name='shownav'),
]

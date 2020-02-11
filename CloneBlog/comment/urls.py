# from django.contrib import admin
from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('add/', views.AddcommentView, name='add_comment'),
]
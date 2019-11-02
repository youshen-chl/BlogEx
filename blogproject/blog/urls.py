#from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('tags/<int:pk>/', views.tags, name='tags'),
]

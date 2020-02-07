
# from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'storm'

urlpatterns = [
    path('', views.hello, name='hello'),
    path('list/', views.showlist, name='showlist'),
    path('nav/', views.shownav1, name='shownav'),
    re_path('category/(?P<bigslug>.*?)/(?P<slug>.*?)', views.shownav, name='category'),
    path('article/<slug:slug>/', views.show_article, name='article'),
    path('date/<int:year>/<int:month>/', views.show_article, name='date'),
    path('tag/<slug:tag>/', views.show_article, name='tag'),
]


# from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'storm'

urlpatterns = [
    path('', views.IndexView.as_view(template_name='index_main.html'), name='index'),
    # path('nav/', views.IndexView.as_view(template_name='index_main.html'), name='shownav'),
    re_path('category/(?P<bigslug>.*?)/(?P<slug>.*?)', views.IndexView.as_view(), name='category'), 
    path('date/<int:year>/<int:month>/', views.IndexView.as_view(), name='date'),
    path('tag/<slug:tag>/', views.IndexView.as_view(), name='tag'),
    path('article/<slug:slug>/', views.ArticleView.as_view(), name='article'),
]

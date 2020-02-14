from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.loginView , name='login'),
    path('logout/', views.logoutView , name='logout'),
    path('register/', views.registerView, name='register'),
    path('profile/', views.profileView, name='profile'),
    path('profile/change/', views.changeProfileView, name='change_profile'),
]
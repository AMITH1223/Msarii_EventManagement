from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_event/', views.register_event, name='register_event'),
]
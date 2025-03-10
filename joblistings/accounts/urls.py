#imports
from django.urls import path
from .views import register
from django.contrib.auth import views as auth_views

#Defining URL patterns for the register, login, and logout page
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
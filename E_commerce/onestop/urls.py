from telnetlib import LOGOUT
from unicodedata import name
from django.urls import path, include
from onestop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.main, name="main"),
    path('landing/', views.landing_page, name="landing"),
    path('signup/',views.signup, name='signup'),
]
from telnetlib import LOGOUT
from unicodedata import name
from django.urls import path, include
from onestop import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.hp, name="hp"),
    path('accounts/', include('allauth.urls')),
    path('landing/', views.landing_page, name="landing"),
]
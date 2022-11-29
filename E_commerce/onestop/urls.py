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
    path('mens/',views.mens_main, name='mens_main_page'),
    path('women/',views.women_main, name='women_main_page'),
    path('kids/',views.kids_main, name='kids_main_page'),
    path('regis/',views.regis, name='regis'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('graph/', views.graph ,name='graph'),
    path('payment/', views.payment ,name='payment'),
    path('trial/', views.trial, name='trial')
]
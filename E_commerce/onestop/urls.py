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
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('graph/', views.graph ,name='graph'),
    path('cart/', views.cart,name='cartPage'),
    path('sellerLogin/', views.sellerLogin,name='sellerLogin'),
    path('customerProfile/', views.customerProfile,name='customerProfile'),
    path('sellerProfile/', views.sellerProfile,name='sellerProfile'),
    path('pr/', views.pr,name='productAdd'),
    path('seller_profile_main/', views.mainSellerProfile,name='main_profile_seller'),
    path('seller_logout/', views.sellerLogout,name='seller_logout'),
    path('viewProduct/', views.viewProduct,name='viewProduct'),
    path('sellerOrders/', views.sellerOrders,name='sellerOrders'),
    path('customerOrders/', views.customerOrders,name='customerOrders'),
]
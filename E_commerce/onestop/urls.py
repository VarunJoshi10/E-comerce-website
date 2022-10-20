from django.urls import path, include
from onestop import views

urlpatterns = [
    path('', views.hp, name="hp"),
    path('accounts/', include('allauth.urls')),
    path('landing/', views.new, name='new'),
]
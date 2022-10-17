from django.urls import path, include
from shopify import views


urlpatterns = [
    path('', views.hp, name="hp")
]

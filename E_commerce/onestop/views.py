from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# For accessing social account model
from allauth.socialaccount.models import SocialAccount

# Create your views here.

def hp(request):
    return render(request, 'main.html')

def landing_page(request):
    return render(request, 'landing.html')

def signup(request):
    return render(request, 'signup.html')
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def hp(request):
    return render(request, 'main.html')

    # user = User.objects()

    # print(user)

    # if User.is_authenticated():
    #     return render(request, 'landing.html')


def landing_page(request):
    return render(request, 'landing.html')

def signup(request):
    return render(request, 'signup.html')
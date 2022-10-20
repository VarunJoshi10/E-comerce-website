import re
from django.shortcuts import render, HttpResponse

# Create your views here.

def hp(request):
    return render(request, 'try.html')

def new(request):
    return render(request, 'landing.html')
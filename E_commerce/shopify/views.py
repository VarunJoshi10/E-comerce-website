from django.shortcuts import render, HttpResponse

# Create your views here.

def hp(request):
    return HttpResponse("This si it")
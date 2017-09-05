from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def first(request):
    return HttpResponse("<h1>Yo dawg!</h1>")

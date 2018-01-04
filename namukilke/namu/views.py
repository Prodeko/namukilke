from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")

def testi(request):
    return HttpResponse("Täältä voi lisätä tuotteen.")

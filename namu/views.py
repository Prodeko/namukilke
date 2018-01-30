from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse

from .models import User, Product


"""Render a list of users for selection"""
class Index(ListView):
    model = User
    template_name = 'namu/index.html'


"""This page might not be needed"""
def user(request):
    return HttpResponse("Hello user!")


class Buy(ListView):
    model = Product
    template_name = 'namu/buy.html'


class Deposit(DetailView):
    model = User
    template_name = 'namu/deposit.html'

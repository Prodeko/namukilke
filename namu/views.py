from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import User, Product
from django.shortcuts import redirect


def redirectToBuy(request, user_id):
	return redirect("./buy")

def redirectToIndex(request):
	return redirect("../")

"""Render a list of users for selection"""

class Index(ListView):
    model = User
    template_name = 'namu/index.html'



"""This page might not be needed"""  # <-- this is correct
# def User(ListView):
#    template_name = 'namu/user.html'

"""Display information about user & allow to purchase items"""


class Buy(ListView):
    model = Product
    template_name = 'namu/buy.html'


"""Let user make deposit. Might need to be detailview?"""


class Deposit(ListView):
    model = User
    template_name = 'namu/deposit.html'

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import User, Product, Transaction, Deposit
from django.db.models import Sum
from django.shortcuts import redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def redirect_to_buy(request, user_id):
    return redirect("./buy")


def redirect_to_index(request):
    return redirect("../")


class Index(ListView):
    """Render a list of users for selection"""
    model = User
    template_name = 'namu/index.html'


class Buy(ListView):
    """Display information about user & allow to purchase items"""
    model = Product
    template_name = 'namu/buy.html'

    def post(self, *args, **kwargs):
        """Buy a given product"""
        u = User.objects.get(pk=self.kwargs['user_id'])
        p = Product.objects.get(pk=self.request.POST['product_id'])
        t = Transaction(product=p, user=u, price=p.price)
        t.save()
        # TODO: check that purchase is indeed succesful (enough funds, etc)
        messages.success(self.request, 'Success - ' + p.name + ' bought!')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))

    def get_balance(self, *args, **kwargs):
        """ Calculate available balance """
        u = User.objects.get(pk=self.kwargs['user_id'])
        transactions = Transaction.objects.filter(user=u).aggregate(sum=Sum('price'))
        deposits = Deposit.objects.filter(user=u).aggregate(sum=Sum('amount'))
        # TODO: handle calculation in situation when either query returns null
        balance = deposits['sum'] - transactions['sum']
        return balance

    def get_context_data(self, *args, **kwargs):
        context = super(Buy, self).get_context_data(**kwargs)
        u = User.objects.get(pk=self.kwargs['user_id'])
        balance = self.get_balance()
        context['user'] = u
        context['balance'] = balance
        return context


class Topup(ListView):
    """Let user make deposit. Might need to be detailview?"""
    model = User
    template_name = 'namu/topup.html'

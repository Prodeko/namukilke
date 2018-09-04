import json
from decimal import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        user_names = {u.name: None for u in users}
        context['user_autocomplete'] = json.dumps(user_names)
        return context


# TODO: form validation: throw error if name > 100 char & warning if name is not unique
class UserCreate(CreateView):
    model = User
    fields = ['name']


class Products(ListView):
    """ List product details & sales numbers. A nice-to-have feature.
        Additions and modifications through django admin or separate log-in to prevent tampering"""
    model = Product
    template_name = 'namu/products.html'


class Buy(ListView):
    """Display information about user & allow to purchase items"""
    model = Product
    template_name = 'namu/buy.html'

    def post(self, *args, **kwargs):
        """Buy a given product"""
        try:
            u = User.objects.get(pk=self.kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404('Account does not exist')
        try:
            p = Product.objects.get(pk=self.request.POST['product_id'])
        except Product.DoesNotExist:
            raise Http404('Product does not exist')

        bal = u.account_balance()
        if bal >= p.price:
            t = Transaction(product=p, user=u, price=p.price)
            t.save()
            messages.success(self.request, 'Success - ' + p.name + ' bought!')
        else:
            messages.error(self.request, 'Error - not enough funds!')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))

    def get_context_data(self, *args, **kwargs):
        context = super(Buy, self).get_context_data(**kwargs)
        try:
            u = User.objects.get(pk=self.kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404('Account does not exist')
        context['user'] = u
        context['balance'] = u.account_balance()
        return context


class Topup(DetailView):
    """Let user make deposit. Might need to be detailview?"""
    model = User
    template_name = 'namu/deposit_form.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *args, **kwargs):
        context = super(Topup, self).get_context_data(**kwargs)
        context['account_balance'] = self.get_object().account_balance()
        context['cash_units'] = [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05]
        return context

    def post(self, *args, **kwargs):
        u = self.get_object()
        d = Deposit(user=u, amount=self.request.POST['amount'], payment_method=self.request.POST['payment_method'])
        d.save()
        messages.success(self.request, 'Success - ' + d.amount + ' euros added to your account!')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))

import json
from decimal import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import Namuseta, User, Product, Transaction, Deposit, Restock
from django.db.models import Q, Sum, Count
from django.shortcuts import redirect, render
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
        users = User.objects.filter(is_active=True)
        user_names = {"{} - {}".format(u.id, u.name): None for u in users}
        context['user_autocomplete'] = json.dumps(user_names)
        n = Namuseta.objects.get(pk=1)
        context['namuseta'] = n
        return context

    # TODO: form validation: throw error if name > 100 char & warning if name is not unique. current FieldError not working
    def post(self, *args, **kwargs):
        new_name = self.request.POST['name']
        try:
            u = User.objects.create(name=new_name)
            u.save()
            messages.success(self.request, 'Account ' + u.name + ' created!')
        except User.FieldError:
            messages.warning(self.request, 'Error - invalid name!')
        return HttpResponseRedirect(reverse('topup', kwargs={'user_id': u.id}))


class Products(ListView):
    """ List product details & sales numbers. A nice-to-have feature.
        Additions and modifications through django admin or separate log-in to prevent tampering"""
    model = Product
    template_name = 'namu/products.html'


class Buy(ListView):
    """Display information about user & allow them to purchase products"""
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
            t = Transaction(product=p, user=u, price=p.price, cost=p.cost)
            t.save()
            messages.info(self.request, p.name + ' bought!')
        else:
            messages.error(self.request, 'Error - not enough funds!')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))

    def get_queryset(self):
        u = User.objects.get(pk=self.kwargs['user_id'])
        if Transaction.objects.filter(user=u).exists():
            user_transaction = Count('transaction', filter=Q(transaction__user=u))
            products = Product.objects.annotate(buy_count=user_transaction)
            active_products = products.filter(is_active=True).order_by('-buy_count')
        else:
            active_products = Product.objects.filter(is_active=True)
        return active_products

    def get_context_data(self, *args, **kwargs):
        context = super(Buy, self).get_context_data(**kwargs)
        try:
            u = User.objects.get(pk=self.kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404('Account does not exist')
        context['user'] = u
        context['balance'] = u.account_balance()
        n = Namuseta.objects.get(pk=1)
        context['namuseta'] = n
        return context


def revert_previous_transaction(request, **kwargs):
    """Create deposit and restock objects to revert previous transaction"""
    if request.method == 'POST':
        try:
            u = User.objects.get(pk=kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404('Account does not exist')
        t = Transaction.objects.filter(user=u).last()
        if t:
            d = Deposit(user=u, amount=t.price, payment_method='r')
            r = Restock(product=t.product, quantity=1, type='r')
            d.save()
            r.save()
            messages.success(request, r.product.name + ' refunded')
        else:
            messages.warning(request, 'Error - No transactions to revert')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))


class Topup(DetailView):
    """Let user make a deposit."""
    model = User
    template_name = 'namu/topup.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *args, **kwargs):
        context = super(Topup, self).get_context_data(**kwargs)
        context['account_balance'] = self.get_object().account_balance()
        context['cash_units'] = [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05]
        n = Namuseta.objects.get(pk=1)
        context['namuseta'] = n
        return context

    def post(self, *args, **kwargs):
        u = self.get_object()
        d = Deposit(user=u, amount=self.request.POST['amount'], payment_method=self.request.POST['payment_method'])
        d.save()
        messages.success(self.request, d.amount + ' euros added to your account!')
        return HttpResponseRedirect(reverse('buy', kwargs={'user_id': u.id}))


def statistics(request, **kwargs):
    """Show basic statistics of topups and purchases."""
    if request.method == 'GET':
        # TODO: multiply quantity with price:
        # restock = Restock.objects.filter(type='s').aggregate(restock_price=Sum('product__price'), restock_cost=Sum('product__cost'))
        #TODO: add time interval
        sales = Transaction.objects.aggregate(sales_price=Sum('price'), sales_cost=Sum('cost'))
        refunds =  Deposit.objects.filter(payment_method='r').aggregate(amount=Sum('amount'))
        deposits = Deposit.objects.filter(Q(payment_method='m') | Q(payment_method='c')).aggregate(amount=Sum('amount'))

        t = Transaction.objects.aggregate(sum=Sum('price'))
        t_sum = t['sum'] or Decimal(0.00)
        d = Deposit.objects.aggregate(sum=Sum('amount'))
        d_sum = d['sum'] or Decimal(0.00)
        balance = round(d_sum - t_sum, 2)

        context = {
            'date_start': 'aloituspvm',
            'date_end': 'lopetuspvm',
            'sales_price': sales['sales_price'],
            'sales_cost': sales['sales_cost'],
            'refunds': refunds['amount'],
            'deposits': deposits['amount'],
            'balance': balance,
        }

        return render(request, 'namu/stats.html', context)
    pass

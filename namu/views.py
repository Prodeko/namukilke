import json
from datetime import datetime
from decimal import *

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Deposit, Namuseta, Product, Restock, Transaction, User


def redirect_to_buy(request, user_id):
    return redirect("./buy")


def redirect_to_index(request):
    return redirect("../")


class Index(ListView):
    """Render a list of users for selection"""

    model = User
    template_name = "namu/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(is_active=True)
        user_names = {"{} - {}".format(u.id, u.name): None for u in users}
        context["user_autocomplete"] = json.dumps(user_names)
        n = Namuseta.objects.get(pk=1)
        context["namuseta"] = n
        return context

    # TODO: form validation: throw error if name > 100 char & warning if name is not unique. current FieldError not working
    def post(self, *args, **kwargs):
        new_name = self.request.POST["name"]
        try:
            u = User.objects.create(name=new_name)
            u.save()
            messages.success(self.request, "Account " + u.name + " created!")
        except User.FieldError:
            messages.warning(self.request, "Error - invalid name!")
        return HttpResponseRedirect(reverse("topup", kwargs={"user_id": u.id}))


class Products(ListView):
    """ List product details & sales numbers. A nice-to-have feature.
        Additions and modifications through django admin or separate log-in to prevent tampering"""

    model = Product
    template_name = "namu/products.html"


class Buy(ListView):
    """Display information about user & allow them to purchase products"""

    model = Product
    template_name = "namu/buy.html"

    def post(self, *args, **kwargs):
        """Buy a given product"""
        try:
            u = User.objects.get(pk=self.kwargs["user_id"])
        except User.DoesNotExist:
            raise Http404("Account does not exist")
        try:
            p = Product.objects.get(pk=self.request.POST["product_id"])
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        bal = u.account_balance()
        if bal >= p.price:
            t = Transaction(product=p, user=u, price=p.price, cost=p.cost)
            t.save()
            messages.info(self.request, p.name + " bought!")
        else:
            messages.error(self.request, "Error - not enough funds!")
        return HttpResponseRedirect(reverse("buy", kwargs={"user_id": u.id}))

    def get_queryset(self):
        u = User.objects.get(pk=self.kwargs["user_id"])
        if Transaction.objects.filter(user=u).exists():
            user_transaction = Count("transaction", filter=Q(transaction__user=u))
            products = Product.objects.annotate(buy_count=user_transaction)
            active_products = products.filter(is_active=True).order_by("-buy_count")
        else:
            active_products = Product.objects.filter(is_active=True)
        return active_products

    def get_context_data(self, *args, **kwargs):
        context = super(Buy, self).get_context_data(**kwargs)
        try:
            u = User.objects.get(pk=self.kwargs["user_id"])
        except User.DoesNotExist:
            raise Http404("Account does not exist")
        context["user"] = u
        context["balance"] = u.account_balance()
        n = Namuseta.objects.get(pk=1)
        context["namuseta"] = n
        return context


def revert_previous_transaction(request, **kwargs):
    """Create deposit and restock objects to revert previous transaction"""
    if request.method == "POST":
        try:
            u = User.objects.get(pk=kwargs["user_id"])
        except User.DoesNotExist:
            raise Http404("Account does not exist")
        t = Transaction.objects.filter(user=u).last()
        if t:
            d = Deposit(user=u, amount=t.price, payment_method="r")
            r = Restock(product=t.product, quantity=1, type="r")
            d.save()
            r.save()
            messages.success(request, r.product.name + " refunded")
        else:
            messages.warning(request, "Error - No transactions to revert")
        return HttpResponseRedirect(reverse("buy", kwargs={"user_id": u.id}))


class Topup(DetailView):
    """Let user make a deposit."""

    model = User
    template_name = "namu/topup.html"
    context_object_name = "user"
    pk_url_kwarg = "user_id"

    def get_context_data(self, *args, **kwargs):
        context = super(Topup, self).get_context_data(**kwargs)
        context["account_balance"] = self.get_object().account_balance()
        context["cash_units"] = [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05]
        n = Namuseta.objects.get(pk=1)
        context["namuseta"] = n
        return context

    def post(self, *args, **kwargs):
        u = self.get_object()
        d = Deposit(
            user=u,
            amount=self.request.POST["amount"],
            payment_method=self.request.POST["payment_method"],
        )
        d.save()
        messages.success(self.request, d.amount + " euros added to your account!")
        return HttpResponseRedirect(reverse("buy", kwargs={"user_id": u.id}))


def statistics(request, **kwargs):
    """Show basic statistics of topups and purchases."""
    if request.method == "GET":

        start = request.GET.get("start", "2018-09-01")
        end = request.GET.get("end", datetime.now().strftime("%Y-%m-%d"))

        # Change in sales, refunds, deposits, and balances
        sales = Transaction.objects.filter(
            timestamp__gte=start, timestamp__lt=end
        ).aggregate(price=Sum("price"), cost=Sum("cost"))
        sales_price = round(sales["price"] or Decimal(0.00), 2)
        sales_cost = round(sales["cost"] or Decimal(0.00), 2)

        refunds = Deposit.objects.filter(
            payment_method="r", timestamp__gte=start, timestamp__lt=end
        ).aggregate(amount=Sum("amount"))
        refunds = round(refunds["amount"] or Decimal(0.00), 2)

        deposits = Deposit.objects.filter(
            Q(payment_method="m") | Q(payment_method="c"),
            timestamp__gte=start,
            timestamp__lt=end,
        ).aggregate(amount=Sum("amount"))
        deposits = round(deposits["amount"] or Decimal(0.00), 2)

        net_sales = sales_price - refunds

        # TODO: Margin should be added " + refunds_cost" in order to be accurate but this is currently not stored in the database
        est_margin = sales_price - refunds - sales_cost

        balances_change = deposits + refunds - sales_price

        # Balances at start
        sales_until_start = Transaction.objects.filter(timestamp__lt=start).aggregate(
            price=Sum("price"), cost=Sum("cost")
        )
        sales_price_until_start = round(sales_until_start["price"] or Decimal(0.00), 2)

        refunds_until_start = Deposit.objects.filter(
            payment_method="r", timestamp__lt=start
        ).aggregate(amount=Sum("amount"))
        refunds_until_start = round(refunds_until_start["amount"] or Decimal(0.00), 2)

        deposits_until_start = Deposit.objects.filter(
            Q(payment_method="m") | Q(payment_method="c"), timestamp__lt=start
        ).aggregate(amount=Sum("amount"))
        deposits_until_start = round(deposits_until_start["amount"] or Decimal(0.00), 2)

        balances_at_start = (
            deposits_until_start + refunds_until_start - sales_price_until_start
        )
        balances_at_end = balances_at_start + balances_change

        # TODO: Inventory values and losses
        # TODO: multiply quantity with price to get restocks. Should store the cost at the time of restock
        # restock = Restock.objects.filter(type='s').aggregate(restock_price=Sum('product__price'), restock_cost=Sum('product__cost'))

        context = {
            "date_start": start,
            "date_end": end,
            "sales_price": sales_price,
            "sales_cost": sales_cost,
            "refunds": refunds,
            "net_sales": net_sales,
            "est_margin": est_margin,
            "deposits": deposits,
            "balances_start": balances_at_start,
            "balances_end": balances_at_end,
            "balances_change": balances_change,
        }

        return render(request, "namu/stats.html", context)
    pass

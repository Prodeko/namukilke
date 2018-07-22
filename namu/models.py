from django.db import models
from django.urls import reverse
from django.db.models import Sum
from decimal import *


class User(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topup', kwargs={'user_id': self.pk})

    def account_balance(self):
        t_sum = Decimal(0.00)
        d_sum = Decimal(0.00)
        if Transaction.objects.filter(user=self).exists():
            t = Transaction.objects.filter(user=self).aggregate(sum=Sum('price'))
            t_sum = t['sum']
        if Deposit.objects.filter(user=self).exists():
            d = Deposit.objects.filter(user=self).aggregate(sum=Sum('amount'))
            d_sum = d['sum']
        balance = d_sum - t_sum
        return balance


class Product(models.Model):
    CATEGORY_OPTIONS = (
        ('z', 'Freezer'),
        ('f', 'Fridge'),
        ('c', 'Cabinet'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_OPTIONS,
        default='c'
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    picture = models.URLField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Deposit(models.Model):
    PAYMENT_METHOD_OPTIONS = (
        ('c', 'Cash'),
        ('m', 'MobilePay'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.CharField(
        max_length=1,
        choices=PAYMENT_METHOD_OPTIONS,
        default='c',
    )


class Restock(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


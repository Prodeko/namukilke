from django.contrib import admin
from .models import User, Product, Transaction, Deposit, Restock


# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Deposit)
admin.site.register(Restock)

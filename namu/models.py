from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)


class Deposit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)


class Restock(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

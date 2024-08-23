from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    # one-2-one relation with user so when user signup customer created for that user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    profile = models.ImageField(null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    # one-2-one relation with user so when user created profile automatically created
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.user_name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    CATEGORY = [
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    ]
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(
        max_length=200, choices=CATEGORY, default='Indoor')
    description = models.CharField(max_length=200, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    ]
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.product.name

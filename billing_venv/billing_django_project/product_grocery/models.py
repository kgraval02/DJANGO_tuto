from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else ''


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_pic')
    description = models.TextField(null=True, blank=True)
    manufacturer = models.CharField(max_length=20, null=True, blank=True)
    unit_added = models.IntegerField(null=True, default=0)
    price = models.FloatField(max_length=100, null=True, blank=True)
    discount = models.FloatField(max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else ''

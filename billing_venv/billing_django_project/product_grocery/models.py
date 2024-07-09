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
    image = models.FileField(null=True, blank=True, upload_to="product_grocery/static/product_pic")
    description = models.TextField(null=True, blank=True)
    manufacturer = models.TextField(null=True, blank=True)
    price = models.FloatField(max_length=100, null=True, blank=True)
    discount = models.FloatField(max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else ''

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default=None, blank=True)
    name = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_grocery/static/images/')
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class Feedback(models.Model):
#     pass

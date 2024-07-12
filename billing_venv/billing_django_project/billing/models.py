from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models
from product_grocery.models import Product, Category


# class CustomUser(AbstractUser):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_approved = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f'Feedback from {self.user.username} on {self.created_at}'

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models
#
# class CustomUser(models.Model):
#     #     REQUIRED_FIELDS = ('password ', 'name ', 'email')
#     is_approved = models.BooleanField(default=0)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user.username

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)

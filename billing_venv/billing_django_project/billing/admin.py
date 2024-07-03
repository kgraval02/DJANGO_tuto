from django.contrib import admin
from .models import Profile
from django.contrib import admin
from django.contrib.auth.models import User  # Import the User model

# Register the User model with the admin

admin.site.register(Profile)

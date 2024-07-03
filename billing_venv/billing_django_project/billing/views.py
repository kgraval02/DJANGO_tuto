from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from product_grocery.models import Product
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

def admin_login(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "Admin login successfully"
                return redirect('dashboard_admin')
            else:
                msg = "Invalid Credentials"
                return redirect('home_page')
        except:
            msg = "Invalid Credentials"
            return redirect('home_page')
    context = {'msg': msg, 'title': 'Admin log in'}
    return render(request, 'admin/admin_login.html', context)

def about(request):
    return render(request,template_name='about.html', context={'title': 'About Page - QUICK CART HUB'})

def b_home(request):
    return render(request,template_name='billing/billing_home.html', context={'title': 'USER DASHBOARD - QUICK CART HUB'})

def home(request):
    data_context = {
        'title': 'Home Page - QUICK CART HUB',
    }
    return render(request, 'home.html', data_context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('user_login2')
    else:
        form = UserRegisterForm()

    data_context = {
        'title': 'User registration page - QUICK CART HUB',
        'form': form,
    }
    return render(request, 'users/register.html', data_context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('user_profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {'u_form': u_form, 'p_form': p_form, 'title' : 'user profile page'}
#
#     return render(request, template_name='users/profile.html', context=context)

def admin_dashboard(request):
    context = {
        'title': 'ADMIN - DASHBOARD'
    }
    return render(request, 'admin/dashboard_admin.html', context)

# def admin_user_view(request):
#     return render(request,template_name='admin/view_users.html', context={'title': 'Users - QUICK CART HUB'})

# Define a new UserAdmin class
# class admin_user_view   (BaseUserAdmin):
#     # Define fields to display in the admin list view
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
#
#     # Add filters for the admin list view
#     list_filter = ('is_staff', 'is_superuser', 'is_active')
#
#     # Add search fields for the admin list view
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#
#     # Define fieldsets to organize the detail view of a user
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#
#     # Customize ordering of users in the admin list view
#     ordering = ('username',)

# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

def admin_user_view(request):
    # Retrieve all users
    users = User.objects.all()
    return render(request, 'admin/view_users.html', {'users': users})

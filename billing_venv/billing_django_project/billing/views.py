from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.http import HttpResponse, request
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def admin_login(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    context = {'msg': msg, 'title': 'Admin log in'}
    return render(request, 'admin/admin_login.html', context)

def about(request):
    return render(request,template_name='about.html', context={'title': 'About Page - QUICK CART HUB'})

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
            return redirect('home_page')
            # return redirect('login')
    else:
        form = UserRegisterForm()

    data_context = {
        'title': 'User registration page - QUICK CART HUB',
        'form': form,
    }
    return render(request, 'users/register.html', data_context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form, 'title' : 'user profile page'}

    return render(request, template_name='users/profile.html', context=context)
#
# def admin_home(request):
#     data_context = {
#         'title': 'Home Page - QUICK CART HUB ADMIN',
#     }
#     return render(request, 'admin/admin_home.html', data_context)

def admin_dashboard(request):
    context = {
        'title': 'ADMIN - DASHBOARD'
    }
    return render(request, 'admin/dashboard_admin.html', context)


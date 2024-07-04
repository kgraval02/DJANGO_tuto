import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import CollectionCart
from product_grocery.models import Product

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

def admin_dashboard(request):
    context = {
        'title': 'ADMIN - DASHBOARD'
    }
    return render(request, 'admin/dashboard_admin.html', context)

def admin_user_view(request):
    # Retrieve all users
    users = User.objects.all()
    return render(request, 'admin/view_users.html', {'use   rs': users})

def addToCart(request, pid):
    myli = {"objects":[]}
    try:
        cart = CollectionCart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = CollectionCart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    cart = CollectionCart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    try:
        cart = CollectionCart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'billing/add_to_cart.html', locals())
def deletecart(request, pid):
    cart = CollectionCart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')
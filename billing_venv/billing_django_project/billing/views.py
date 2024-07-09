import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from billing.forms import UserRegisterForm

def home(request):
    data_context = {
        'title': 'Home Page - QUICK CART HUB',
    }
    return render(request, 'home.html', data_context)
def about(request):
    return render(request,template_name='about.html', context={'title': 'About Page - QUICK CART HUB'})
@staff_member_required
def userlist(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'users of QUICK CART HUB'
    }
    return render(request, template_name='admin/manage_user.html', context=context)

class Admin_login(LoginView):
    template_name = 'admin/admin_login.html'
    success_url = reverse_lazy('dashboard_admin')
    def get_success_url(self):
        return self.success_url

class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard_admin.html'
class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login_user')
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_approved = False
        user.save()
        return super().form_valid(form)

# class UserLoginView(LoginView):
#     template_name = 'users/login.html'
#     success_url = reverse_lazy('bill_user_home')
#     def form_valid(self, form):
#         user = form.get_user()
#         if user.is_approved:
#             login(self.request, user)
#             return self.success_url
#
#         else:
#             messages.error(self.request, 'Your account is not approved yet.')
#             return redirect('login_user')
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('bill_user_home')
    def get_success_url(self):
        return self.success_url

class UserDashHome(TemplateView):
    template_name = 'billing/billing_home.html'
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    def get_next_page(self):
        if self.request.user.is_staff:
            return 'home_page'
        return 'home_page'
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_pass.html'
    success_url = reverse_lazy('bill_user_home')
    def form_valid(self, form):
        messages.success(self.request, "Password Changed")
        return super().form_valid(form)
    def form_invalid(self, form):
        if 'old_password' in form.errors:
            messages.error(self.request, "Invalid Password")
        elif 'new_password2' in form.errors:
            messages.error(self.request, "Password not matching")
        return super().form_invalid(form)



# cart_add
# item_clear
# item_increment
# item_decrement
# cart_clear
# cart_detail
#
# @login_required(login_url="login_user")
# def cart_add(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("bill_user_home")
#
# @login_required(login_url="login_user")
# def item_clear(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.remove(product)
#     return redirect("cart_detail")
#
# @login_required(login_url="login_user")
# def item_increment(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.add(product=product)
#     return redirect("cart_detail")
#
# @login_required(login_url="login_user")
# def item_decrement(request, id):
#     cart = Cart(request)
#     product = Product.objects.get(id=id)
#     cart.decrement(product=product)
#     return redirect("cart_detail")
#
# @login_required(login_url="login_user")
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")
#
# @login_required(login_url="login_user")
# def cart_detail(request):
#     return render(request, 'billing/cart.html')
#

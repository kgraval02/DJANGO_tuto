from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render
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
        response = super().form_valid(form)
        # Additional actions after a valid form can be handled here
        return response
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('bill_user_home')
    def get_success_url(self):
        return self.success_url
class UserDashHome(TemplateView):
    template_name = 'billing/billing_home.html'
class CustomLogoutView(LogoutView):
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

from urllib import request

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admin Login'
        return context

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.add_error(None, 'You do not have permission to access this page.')
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard_admin.html'


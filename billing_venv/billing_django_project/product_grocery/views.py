# from django.core.checks import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from pyexpat.errors import messages
from .models import Category, Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# ,Feedback

# category
class Add_category(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('view_cate')

class View_category(ListView):
    model = Category
    template_name = 'category/view_category.html'
    context_object_name = 'cate'
    # paginate_by = 2

class Edit_category(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     if self.request.user == is_staff:
    #         return True


class Delete_category(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = 'view_cate'

    # def test_func(self):
    #     if self.request.user == is_staff:
    #         return True

# product
class Add_product(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'discount', 'category', 'description', 'manufacturer', 'image']
    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('view_prdt')

class View_product(ListView):
    model = Product
    template_name = 'product/product_view.html'
    context_object_name = 'product'

class Product_detail(DetailView):
    model = Product

class Edit_product(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'image']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     if self.request.user == is_staff:
    #         return True


class Delete_product(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = 'view_prdt'

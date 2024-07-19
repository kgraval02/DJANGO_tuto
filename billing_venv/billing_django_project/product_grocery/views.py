from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Category, Product
from .forms import CategoryForm, ProductForm


# category
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/add_category.html'
    success_url = reverse_lazy('view_category')  # Assuming you have a category list view


class CategoryListView(ListView):
    model = Category
    template_name = 'category/view_category.html'
    context_object_name = 'categories'


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/edit_category.html'
    success_url = reverse_lazy('view_category')
    context_object_name = 'category'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete_category.html'
    success_url = reverse_lazy('view_category')


# products
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_add.html'
    success_url = reverse_lazy('view_product')  # Adjust this URL as necessary

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product added")
        return response


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_view.html'
    context_object_name = 'products'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'
    success_url = reverse_lazy('view_product')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product Updated")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('view_product')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Product Deleted")
        return response


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail_product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

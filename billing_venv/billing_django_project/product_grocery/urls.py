from django.urls import path
from .views import (CategoryCreateView, CategoryListView, CategoryUpdateView, ProductUpdateView, ProductDeleteView, ProductDetailView,
                    CategoryDeleteView, ProductCreateView, ProductListView)

urlpatterns = [
    path('category_add/', CategoryCreateView.as_view(), name='add_category'),
    path('category_view/', CategoryListView.as_view(), name='view_category'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('product_add/', ProductCreateView.as_view(), name='add_product'),
    path('products/', ProductListView.as_view(), name='view_product'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pid>/', ProductDetailView.as_view(), name='detail_product'),

]



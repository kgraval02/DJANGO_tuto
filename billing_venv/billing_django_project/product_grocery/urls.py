from django.urls import path, include
from . import views

urlpatterns = [
    path('add_category/', views.Add_category.as_view(template_name='category/add_category.html'), name='add_cate'),
    path('view_category/', views.View_category.as_view(), name='view_cate'),
    path('edit_category/<int:pk>/', views.Edit_category.as_view(template_name='category/edit_category.html'), name='update_cate'),
    path('delete_category/<int:pk>/', views.Delete_category.as_view(template_name='category/delete_category.html'), name='delete_cate'),
    path('add_product/', views.Add_product.as_view(template_name='product/product_add.html'), name='add_prdt'),
    path('view_product/', views.View_product.as_view(template_name='product/product_view.html'), name='view_prdt'),
    path('view_product1/<int:pk>/', views.Product_detail.as_view(template_name='product/detail_product.html'), name='view_detail_prdt'),
    path('edit_product/<int:pk>/', views.Edit_product.as_view(template_name='product/product_update.html'), name='edit_prdt'),
    path('delete_product/<int:pk>/', views.Delete_product.as_view(template_name='product/product_confirm_delete.html'), name='delete_prdt'),
]

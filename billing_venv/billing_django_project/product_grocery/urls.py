from django.urls import path, include
from . import views

urlpatterns = [
    path('add_category/', views.Add_category.as_view(template_name='category/add_category.html'), name='add_cate'),
    path('view_category/', views.View_category.as_view(), name='view_cate'),
    path('edit_category/', views.Edit_category.as_view(template_name='category/edit_category.html'), name='update_cate'),
    path('delete_category/', views.Delete_category.as_view(template_name='category/delete_category.html'), name='delete_cate'),
    path('add_product/', views.Add_product.as_view(template_name='product/product_add.html'), name='add_prdt'),
    path('view_product/', views.View_product.as_view(template_name='product/product_view.html'), name='view_prdt'),
    path('edit_product/', views.Edit_product.as_view(template_name='product/product_update.html'), name='edit_prdt'),
    path('delete_product/', views.Delete_product.as_view(), name='delete_prdt'),
]

# complete details of product : Product_detail(DetailView):

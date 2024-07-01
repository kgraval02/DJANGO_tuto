from django.urls import path, include
from . import views

urlpatterns = [
    path('product/', views.home, name='product_base'),
    # path('user_register/', views.register, name='register'),
]
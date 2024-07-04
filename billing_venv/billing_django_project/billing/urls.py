from django.urls import path, include
from . import views
from django.contrib.auth import views as user_views
urlpatterns = [
    # path('', include('grocery_product.urls')),
    # path('admin_home/', views.admin_home, name='admin_home_page'),
    path('', views.home, name='home_page'),
    path('about/', views.about, name='about_page'),
    path('billing_home/', views.b_home, name='b_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard_admin/', views.admin_dashboard, name='dashboard_admin'),
    path('user_register/', views.register, name='register'),
    path('user_login/', user_views.LoginView.as_view(template_name='users/login.html'), name='user_login2'),
    path('user_logout/', user_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('user_view/', views.admin_user_view, name='user_view'),
    path('add-to-cart/<int:pid>/', views.addToCart, name="addToCart"),
    path('cart/', views.cart, name="cart"),
    path('incredecre/<int:pid>/', views.incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', views.deletecart, name="deletecart"),


]


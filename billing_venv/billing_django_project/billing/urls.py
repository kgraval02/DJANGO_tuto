from django.urls import path
from . import views
from django.contrib.auth import views as user_views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('user_register/', views.register, name='register'),
    path('user_login/', user_views.LoginView.as_view(template_name='users/login.html'), name='user_login2'),

]
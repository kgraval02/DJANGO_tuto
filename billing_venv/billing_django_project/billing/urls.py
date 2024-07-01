from django.urls import path, include
from . import views
from django.contrib.auth import views as user_views

urlpatterns = [
    # path('', include('grocery_product.urls')),
    # path('admin_home/', views.admin_home, name='admin_home_page'),
    path('', views.home, name='home_page'),
    path('about/', views.about, name='about_page'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard_admin/', views.admin_dashboard, name='dashboard_admin'),
    path('user_register/', views.register, name='register'),
    path('user_login/', user_views.LoginView.as_view(template_name='users/login.html'), name='user_login2'),
    path('user_logout/', user_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='user_profile'),

]

# path('pass_reset/', auth_views.PasswordResetView.as_view(template_name='users/changepass.html'),
#      name='change_pass'),
# path('pass_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/changepass.html'),
#      name='password_reset_done'),
# path('pass_reset_confirm/<uidb64>/<token>/',
#      auth_views.PasswordResetConfirmView.as_view(template_name='users/pass_change_confirm.html'),
#      name='password_reset_confirm'),
# path('pass_reset_complete/',
#      auth_views.PasswordResetCompleteView.as_view(template_name='users/change_pass_complete.html'),
#      name='password_reset_complete'),

from django.urls import path
from billing import views as b_view

urlpatterns = [
    path('', b_view.home, name='home_page'),
    path('about/', b_view.home, name='about_page'),
    path('admin_login/', b_view.Admin_login.as_view(), name='admin_login'),
    path('dashboard_admin/', b_view.AdminDashboardView.as_view(), name='dashboard_admin'),

]

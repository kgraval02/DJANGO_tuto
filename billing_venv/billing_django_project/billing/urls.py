from django.urls import path
from billing import views as b_view

urlpatterns = [
    path('', b_view.home, name='home_page'),
    path('about_quickcarthub/', b_view.about, name='about_page'),
    path('admin_login/', b_view.Admin_login.as_view(), name='admin_login'),
    path('dashboard_admin/', b_view.AdminDashboardView.as_view(), name='dashboard_admin'),
    path('user_reegister/', b_view.RegisterUser.as_view(), name='register_user'),
    path('user_login/', b_view.UserLoginView.as_view(), name='login_user'),
    path('user_home/', b_view.UserDashHome.as_view(), name='bill_user_home'),
    path('logout/', b_view.CustomLogoutView.as_view(), name='logout'),
    path('change_password/', b_view.CustomPasswordChangeView.as_view(), name='changepass'),

]


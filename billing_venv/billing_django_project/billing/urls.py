from django.urls import path
from billing import views as b_view
# from .models import Cart
urlpatterns = [
    path('', b_view.home, name='home_page'),
    path('about_quickcarthub/', b_view.about, name='about_page'),
    path('logout/', b_view.CustomLogoutView.as_view(), name='logout'),
    path('change_password/', b_view.CustomPasswordChangeView.as_view(), name='changepass'),

    path('admin_login/', b_view.AdminLogin.as_view(), name='admin_login'),
    path('dashboard_admin/', b_view.AdminDashboardView.as_view(), name='dashboard_admin'),
    path('user_for_admin/', b_view.userlist, name='usersforadmin'),

    path('user_aproval/<int:user_id>/', b_view.approve_user, name='approve_user'),
    path('user_removal/<int:user_id>/', b_view.reject_user, name='reject_user'),
    path('user_delete/<int:user_id>/', b_view.delete_user, name='delete_user'),

    path('manage_feedback/', b_view.manage_feedback, name='manage_feedback'),
    path('review_feedback/<int:feedback_id>/', b_view.review_feedback, name='review_feedback'),
    path('delete_feedback/<int:feedback_id>/', b_view.delete_feedback, name='delete_feedback'),

    path('user_reegister/', b_view.RegisterUser.as_view(), name='register_user'),
    path('user_login/', b_view.UserLoginView.as_view(), name='login_user'),
    path('user_home/', b_view.UserDashHome.as_view(), name='bill_user_home'),

    path('submit_feedback/', b_view.submit_feedback, name='submit_feedback'),
    path('feedback_thanks/', b_view.feedback_thanks, name='feedback_thanks'),


]




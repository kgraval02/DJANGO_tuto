from django.urls import path
from .views import PostListView, PostDetailsView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog_home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user_post'),
    path('post/<int:pk>/', PostDetailsView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(template_name='blog/post_delete.html'), name='post_delete'),
    path('about/', views.about, name='blog_about'),
]



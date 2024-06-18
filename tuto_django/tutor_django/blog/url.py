from django.urls import path
from .models import PostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog_home'),
    path('about/', views.about, name='blog_about'),
]


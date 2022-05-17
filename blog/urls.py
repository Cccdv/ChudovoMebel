from django.contrib import admin
from django.urls import path
from .views import Blog, BlogDetail, AddPost, UpdatePost, DeletePost

urlpatterns = [
    path('', Blog.as_view(), name="blog"),
    path('article/<int:pk>', BlogDetail.as_view(), name='blog-article'),
    path('add_post/', AddPost.as_view(), name="add_post"),
    path('article/edit/<int:pk>', UpdatePost.as_view(), name="update_post"),
    path('article/<int:pk>/delete', DeletePost.as_view(), name="delete_post"),
]

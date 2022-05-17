from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, EditForm
from django.urls import reverse_lazy

# Create your views here.


class Blog(ListView):
    """Data model class"""
    model = Post
    template_name = 'blog.html'
    ordering = ['-id']


class BlogDetail(DetailView):
    """Data model class"""
    model = Post
    template_name = 'blog_details.html'


class AddPost(CreateView):
    """Data model class"""
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'


class UpdatePost(UpdateView):
    """Data model class"""
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'


class DeletePost(DeleteView):
    """Data model class"""
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('blog')

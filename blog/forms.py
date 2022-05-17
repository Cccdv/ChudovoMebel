from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        """Adding a blog post form"""
        model = Post
        fields = ('title', 'author', 'body', 'header_image')

        """Which input fields can be added"""
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        """Editing a blog post form"""
        model = Post
        fields = ('title', 'body')

        """Which input fields can be edited"""
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

from django import forms

from blog.models import Blog
from catalog.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """Blog form for storing"""
    class Meta:
        model = Blog
        fields = ['title', 'content', 'preview_image']

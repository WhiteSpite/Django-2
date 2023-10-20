from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['title', 'content', 'author', 'post_type', 'categories']
       widgets = {
         'title' : forms.TextInput(attrs={
           'class': 'form-control',
           'placeholder': 'Enter product name'
         }),
         'content' : forms.Textarea(attrs={
           'type': 'number',
           'class': 'form-control',
           'value' : 0
         }),
         'author' : forms.Select(attrs={
           'class': 'form-control',
         }),
         'post_type' : forms.Select(attrs={
           'class': 'form-control',
         }),
         'categories' : forms.SelectMultiple(attrs={
           'class': 'form-control',
         }),
       }
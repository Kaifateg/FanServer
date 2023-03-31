from django import forms
from django.forms import ClearableFileInput

from .models import Post, Reply


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'media': ClearableFileInput(attrs={'multiple': True})}


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = '__all__'

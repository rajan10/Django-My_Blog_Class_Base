from django import forms
from .models import Post, Comment
from django.forms import ModelForm, Textarea
from .import models
from django.db import models


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','image','content']
        widgets ={
            'content':Textarea(attrs={'cols':50,'rows':10})
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        widgets={
            'content':Textarea(attrs={'cols':50, 'rows':10})
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from django import forms
from .models import Post, Comment

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User  # Импортируйте модель пользователя
        fields = ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
from django.forms import ModelForm
from . import models
from django.contrib.auth.forms import UserCreationForm 
from django import forms  
from django.contrib.auth.models import User 

class PostForm(ModelForm):

    class Meta:
        model=models.Post
        fields=["text"]

class ProfileForm(ModelForm):

    class Meta:
        model=models.Profile
        fields="__all__"


class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')  
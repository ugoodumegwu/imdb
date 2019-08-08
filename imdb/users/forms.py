from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

    class Meta:
        model = MyUserModel
        fields = ('username', 'password1', 'password2')
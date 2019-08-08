from django.shortcuts import render

# registration views

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm

class RegisterView(CreateView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('core:MovieList')



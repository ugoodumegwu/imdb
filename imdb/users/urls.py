from django.urls import path, include
from .views import *
import django.contrib.auth.urls
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'users'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
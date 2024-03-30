from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Import your CustomUser model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Update to CustomUser
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser  # Update to CustomUser

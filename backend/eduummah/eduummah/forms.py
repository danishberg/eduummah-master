from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Specify which fields should be used. Exclude 'username'.
        fields = ('email', 'password1', 'password2')

    # Ensure email is treated as a unique identifier.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

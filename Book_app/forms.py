from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

   
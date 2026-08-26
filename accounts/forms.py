from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    class Meta:
        model = Customer
        fields = ("username", "email", "phone", "password1", "password2", "address")

class LoginForm(forms.Form):
    identifier = forms.CharField(label="Email or phone")
    password = forms.CharField(widget=forms.PasswordInput)

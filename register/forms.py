from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(min_length=1)
    last_name = forms.CharField(min_length=1)
    email = forms.EmailField()
    phone = forms.CharField(max_length=9, min_length=9, label="Phone number")
    street = forms.CharField(min_length=1)
    zip_code = forms.CharField(max_length=5, min_length=5)
    city = forms.CharField(min_length=1)

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "phone", "street", "zip_code", "city", "password1", "password2"]

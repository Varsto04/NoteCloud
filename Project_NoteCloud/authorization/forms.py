from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    username = forms.CharField(
        label='Имя пользователя',
        strip=False,
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

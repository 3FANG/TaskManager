from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django import forms


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """Переопределенная форма регистрации пользователя."""

    # UserCreationForm просит только username и password,
    # а мне нужен еще first_name и last_name
    # Также хочу изменить help_text у полей ввода

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserUpdateForm(UserChangeForm):
    """Переопределенная форма обновления данных пользователя."""

    password = None
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

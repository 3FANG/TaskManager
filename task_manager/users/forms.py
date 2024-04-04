from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """Переопределенная форма регистрации пользователя."""

    # UserCreationForm просит только username и password, а мне нужен еще first_name и last_name
    # Также хочу изменить help_text у полей ввода 

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

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


# class DeleteUserForm(forms.Form):
#     """Форма для удаления пользователя с подтврждением при помощи пароля."""
    
#     password = forms.CharField(
#         label="Пароль",
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
#     )

#     error_messages = {
#         "invalid_login": 
#             "Please enter a correct %(username)s and password. Note that both "
#             "fields may be case-sensitive."
#         ,
#         "inactive": "This account is inactive.",
#     }

#     def __init__(self, request=None, *args, **kwargs):
#         """
#         The 'request' parameter is set for custom auth use by subclasses.
#         The form data comes in via the standard 'data' kwarg.
#         """
#         self.request = request
#         self.user_cache = None
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         username = self.request.user.username
#         password = self.cleaned_data.get("password")

#         if username is not None and password:
#             self.user_cache = authenticate(
#                 self.request, username=username, password=password
#             )
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data
    
#     def confirm_login_allowed(self, user):
#         """
#         Controls whether the given User may log in. This is a policy setting,
#         independent of end-user authentication. This default behavior is to
#         allow login by active users, and reject login by inactive users.

#         If the given user cannot log in, this method should raise a
#         ``ValidationError``.

#         If the given user may log in, this method should return None.
#         """
#         if not user.is_active:
#             raise ValidationError(
#                 self.error_messages["inactive"],
#                 code="inactive",
#             )

#     def get_invalid_login_error(self):
#         return ValidationError(
#             self.error_messages["invalid_login"],
#             code="invalid_login",
#             params={"username": self.request.user.username},
#         )
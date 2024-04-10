from django.shortcuts import render
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _


class HomePageView(View):
    """Класс-представление для домашней страницы."""

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class LoginUserView(SuccessMessageMixin, LoginView):
    """Класс-представление для входа пользователя."""

    authentication_form = AuthenticationForm
    template_name = 'login.html'
    success_message = _("You have successfully logged in.")


class LogoutUserView(LogoutView):
    """Класс-представление для выхода пользователя."""

    def post(self, request, *args, **kwargs):
        resposne = super().post(request, *args, **kwargs)
        messages.info(request, _("You've logged out of your account."))
        return resposne

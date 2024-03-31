from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
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
    success_message = _("You have successfully logged in.") # "Вы успешно авторизовались."


class LogoutUserView(LogoutView):
    """Класс-представление для выхода пользователя."""

    # LogoutView calls the logout method and the logout method calls request.session.flush()
    # which will delete any messages when using the SessionStorage backend.
    # You could either move to using the CookieStorage backend,
    # as I don't think this would be affected by request.session.flush
    # 
    # https://stackoverflow.com/questions/59593854/display-messages-on-logoutview

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _("You've logged out of your account.")) # 'Вы вышли из аккаунта.'
        return response

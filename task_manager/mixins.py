from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from task_manager.settings import DANGER
        

class PleaseLoginMixin(LoginRequiredMixin):
    """Тот же LoginRequiredMixin, но добавляет сообщение."""

    error_message = _("You are not logged in! Please log in.") # Вы не авторизованы! Пожалуйста, выполните вход.

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, DANGER, self.error_message)
        return super().dispatch(request, *args, **kwargs)


class OwnerTestMixin(PleaseLoginMixin, UserPassesTestMixin):
    """Миксин, проверяющий, является ли пользователь владельцем аккаунта.

    Также проверяет, аутентифицирован ли пользователь,
    в противном случае отправляет на страницу авторизации.
    """
    
    def test_func(self):
        obj = self.get_object()
        if obj != self.request.user:
            messages.add_message(self.request, DANGER, self.error_message)
            return False
        return True
    
    # Костыль, чтобы вместо ошибки 403 перенаправлял на страницу со всеми пользователями
    def handle_no_permission(self):
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            return redirect('all_users')

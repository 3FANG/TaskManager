from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from task_manager.settings import DANGER


class OwnerTestMixin(LoginRequiredMixin, UserPassesTestMixin):
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
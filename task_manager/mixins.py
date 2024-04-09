from abc import abstractmethod

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib import messages

from task_manager.settings import DANGER
        

class PleaseLoginMixin(LoginRequiredMixin):
    """Тот же LoginRequiredMixin, но добавляет сообщение."""

    error_message = _("You are not logged in! Please log in.") # Вы не авторизованы! Пожалуйста, выполните вход.

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, DANGER, self.error_message)
        return super().dispatch(request, *args, **kwargs)


class OwnerTestMixin(UserPassesTestMixin):
    # Может просто переопределить dispatch(), а не наследовать UserPassesTestMixin,
    # использовать test_func(), а затем обрабатывать возникновние ошибки в handle_no_permission?
    #
    # Также может вместо переопределения get_owner() у дочерних классов сделать функцию-диспетчер для 
    # определения типа модели и возращения соответствующего поля, отвечающего за владельца?
    """Миксин, проверяющий, является ли пользователь владельцем аккаунта.

    Также проверяет, аутентифицирован ли пользователь,
    в противном случае отправляет на страницу авторизации.
    """
    error_access_owner_message = _("You do not have permissions to delete another user.")
    redirect_path = reverse_lazy("all_users")

    @abstractmethod
    def get_owner(self):
        return None
    
    def test_func(self):
        obj = self.get_owner()
        if obj != self.request.user:
            messages.add_message(self.request, DANGER, self.error_access_owner_message)
            return False
        return True
    
    # Костыль, чтобы вместо ошибки 403 перенаправлял на страницу со всеми пользователями
    def handle_no_permission(self):
        try:
            return super().handle_no_permission()
        except PermissionDenied:
            return redirect(self.redirect_path)


class ProtectedInstanceDeleteMixin:
    """Обработка ошибки, связанной с удалением связанного поля.
    
    В случае возникновения ошибки выводит сообщение и выполняет редирект на указанную страницу.
    """

    protected_instance_error_message = _("Error message for deleting a linked entity.")
    protected_instance_error_redirect = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, *kwargs)
        except ProtectedError:
            messages.add_message(request, DANGER, self.protected_instance_error_message)
            return redirect(self.protected_instance_error_redirect)

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import UserRegisterForm
from task_manager.mixins import (
    OwnerTestMixin,
    PleaseLoginMixin,
    ProtectedInstanceDeleteMixin
)


User = get_user_model()


class RegisterUserView(SuccessMessageMixin, CreateView):
    """Класс-представление для регистрации пользователя."""

    form_class = UserRegisterForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login_user')
    success_message = _("User have been successfully signed in.")


class GetUsersView(ListView):
    """Класс-представление выводящий всех пользователей."""

    model = User
    context_object_name = "users_list"
    template_name = "users/index.html"

    def get_queryset(self):
        """Вывод всех пользователей, кроме персонала."""
        return self.model._default_manager.filter(is_staff=False)


class UserUpdateView(PleaseLoginMixin, OwnerTestMixin, SuccessMessageMixin, UpdateView):
    """Класс-представление для редактирования отдельного пользователя."""

    model = User
    form_class = UserRegisterForm
    pk_url_kwarg = "user_id"
    success_url = reverse_lazy('all_users')
    template_name = "users/update.html"
    success_message = _("The user data has been successfully changed.")
    error_access_owner_message = _("You don't have permissions to modify another user.")

    def get_owner(self):
        """Возвращает владельца акакунта."""
        return self.get_object()


class UserDeleteView(
    PleaseLoginMixin,
    OwnerTestMixin,
    SuccessMessageMixin,
    ProtectedInstanceDeleteMixin,
    DeleteView
):
    """Класс-представление для удаление отдельного пользователя."""

    model = User
    pk_url_kwarg = "user_id"
    success_url = reverse_lazy('all_users')
    template_name = "users/delete.html"
    success_message = _("User successfully deleted.")
    on_del_message = _("You can't delete a user because they are associated with tasks.")
    on_del_redirect = reverse_lazy("all_users")

    def get_owner(self):
        """Возвращает владельца акакунта."""
        return self.get_object()

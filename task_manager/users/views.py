from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import get_messages

from task_manager.users.forms import UserRegisterForm
from task_manager.mixins import OwnerTestMixin
# from task_manager.users.forms import DeleteUserForm


User = get_user_model()


class RegisterUserView(SuccessMessageMixin, CreateView):
    """Класс-представление для регистрации пользователя."""

    form_class = UserRegisterForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login_user')
    success_message = _("You have been successfully signed in.") # 'Вы успешно зарегистрированы.'


class GetUsersView(ListView):
    """Класс-представление выводящий всех пользователей."""

    model = User
    context_object_name = "users_list"
    template_name = "users/index.html"


class UserUpdateView(OwnerTestMixin, SuccessMessageMixin, UpdateView):
    """Класс-представление для редактирования отдельного пользователя."""

    model = User
    fields = ['first_name', 'last_name', 'username',]
    pk_url_kwarg = "user_id"
    success_url = reverse_lazy('all_users')
    template_name = "users/update.html"
    success_message = _("The user data has been successfully changed.")
    error_message = _("You don't have permissions to modify another user.") # "У вас нет прав для изменения другого пользователя."


class UserDeleteView(OwnerTestMixin, SuccessMessageMixin, DeleteView):
    """Класс-представление для удаление отдельного пользователя."""

    model = User
    # form_class = DeleteUserForm
    pk_url_kwarg = "user_id"
    success_url = reverse_lazy('all_users')
    template_name = "users/delete.html"
    success_message = _("User successfully deleted.")
    error_message = _("You do not have permissions to delete another user.") # "У вас нет прав для удаления другого пользователя."

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["request"] = self.request
    #     return kwargs


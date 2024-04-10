from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Statuses
from task_manager.mixins import PleaseLoginMixin, ProtectedInstanceDeleteMixin


class CreateStatusView(PleaseLoginMixin, SuccessMessageMixin, CreateView):
    """Класс-представление для создания новго статуса."""

    model = Statuses
    fields = ["name"]
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('all_statuses')
    success_message = _("Status successfully created.")


class IndexStatusesView(PleaseLoginMixin, ListView):
    """Класс-представление, выводящий все статусы."""

    model = Statuses
    context_object_name = 'statuses_list'
    template_name = 'statuses/index.html'


class UpdateStatusView(PleaseLoginMixin, SuccessMessageMixin, UpdateView):
    """Класс-представление для изменения данных статуса."""

    model = Statuses
    fields = ["name"]
    pk_url_kwarg = 'status_id'
    success_url = reverse_lazy('all_statuses')
    template_name = 'statuses/update.html'
    success_message = _("Status has been successfully changed.")


class DeleteStatusView(
    PleaseLoginMixin,
    SuccessMessageMixin,
    ProtectedInstanceDeleteMixin,
    DeleteView
):
    """Класс-представление для удаления статуса."""

    model = Statuses
    pk_url_kwarg = 'status_id'
    success_url = reverse_lazy('all_statuses')
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_message = _("Status has been successfully deleted.")
    on_del_redirect = reverse_lazy("all_statuses")
    on_del_message = _("You can't delete a status because it's associated with tasks.")

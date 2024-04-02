from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Statuses
from task_manager.mixins import PleaseLoginMixin
from task_manager.settings import DANGER


class CreateStatusView(PleaseLoginMixin, SuccessMessageMixin, CreateView):
    """Класс-представление для создания новго статуса."""

    model = Statuses
    fields = ["name"]
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('all_statuses')
    success_message = _("Status successfully created.") # Статус успешно создан.


class GetStatusesView(PleaseLoginMixin, ListView):
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
    context_object_name = 'status'
    success_message = _("Status has been successfully changed.") # Статус успешно обновлен.


class DeleteStatusView(PleaseLoginMixin, SuccessMessageMixin, DeleteView):
    """Класс-представление для удаления статуса."""

    model = Statuses
    pk_url_kwarg = 'status_id'
    success_url = reverse_lazy('all_statuses')
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_message = _("Status has been successfully deleted.") # Статус успешно удален.

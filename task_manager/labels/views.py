from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.labels.models import Labels
from task_manager.mixins import PleaseLoginMixin, ProtectedInstanceDeleteMixin


class CreateLabelView(PleaseLoginMixin, SuccessMessageMixin, CreateView):
    """Класс-представление для создание метки."""

    model = Labels
    fields = ["name"]
    success_url = reverse_lazy("all_labels")
    success_message = _("Label successfully created.")
    template_name = "labels/create.html"


class IndexLabelsView(PleaseLoginMixin, ListView):
    """Класс-представление для вывода всех меток."""

    model = Labels
    context_object_name = "labels_list"
    template_name = "labels/index.html"


class UpdateLabelView(PleaseLoginMixin, SuccessMessageMixin, UpdateView):
    """Класс-представление для обновления метки."""

    model = Labels
    fields = ["name"]
    pk_url_kwarg = "label_id"
    success_url = reverse_lazy("all_labels")
    success_message = _("Label has been successfully changed.")
    template_name = "labels/update.html"


class DeleteLabelView(
    PleaseLoginMixin,
    ProtectedInstanceDeleteMixin,
    SuccessMessageMixin, DeleteView
):
    """Класс-представление для удаления метки"""

    model = Labels
    pk_url_kwarg = "label_id"
    context_object_name = "label"
    success_url = reverse_lazy("all_labels")
    success_message = _("The label has been successfully removed.")
    template_name = "labels/delete.html"
    on_del_redirect = reverse_lazy("all_labels")
    on_del_message = _("You can't delete a label because it's associated with tasks.")

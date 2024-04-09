from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks
from task_manager.tasks.forms import TaskCreationForm, FilterTasksForm
from task_manager.mixins import PleaseLoginMixin, OwnerTestMixin, ProtectedInstanceDeleteMixin
from task_manager.tasks.filters import TasksFilter


# class IndexTasksView(PleaseLoginMixin, FormMixin, ListView):
#     """Класс-представление, выводящий все задачи и форму для фильтрации."""

#     model = Tasks
#     form_class = FilterTasksForm
#     success_url = reverse_lazy('all_tasks')
#     context_object_name = "tasks_list"
#     template_name = "tasks/index.html"

#     def get_queryset(self):
#         """Берем параметры из строки запроса и фильтруем полученные задачи."""
#         queryset = self.model._default_manager.all()
#         status = self.request.GET.get('status')
#         executor = self.request.GET.get('executor')
#         labels = self.request.GET.get('labels')

#         if status:
#             queryset = queryset.filter(status__id=status)
#         if executor:
#             queryset = queryset.filter(executor__id=executor)
#         if labels:
#             queryset = queryset.filter(labels__id=labels)

#         return queryset
    
#     def get_initial(self):
#         """Возвращает исходные данные для формы."""
#         initial = {
#             'status': self.request.GET.get('status'),
#             'executor': self.request.GET.get('executor')
#         }
#         return initial


class IndexTasksView(PleaseLoginMixin, FilterView):
    """Класс-представление, выводящий все задачи и форму для фильтрации."""

    template_name = "tasks/index.html"
    model = Tasks
    context_object_name = "tasks_list"
    filterset_class = TasksFilter


class ShowTaskView(PleaseLoginMixin, DetailView):
    """Класс-представление для просмотра конкретной задачи."""
    
    model = Tasks
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    template_name = 'tasks/show.html'
    

class CreateTaskView(PleaseLoginMixin, SuccessMessageMixin, CreateView):
    """Класс-представление для создания новой задачи."""

    form_class = TaskCreationForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy('all_tasks')
    success_message = _("The task has been successfully created.")

    def form_valid(self, form):
        """Автоматически присваиваем создаваемой задаче владельца."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(PleaseLoginMixin, SuccessMessageMixin, UpdateView):
    """Класс-представление для обновления задачи."""

    model = Tasks
    # fields = ["name", "description", "status", "executor", "labels"]
    form_class = TaskCreationForm
    pk_url_kwarg = 'task_id'
    template_name = 'tasks/update.html'
    context_object_name = 'task'
    success_message = _("The task has been successfully updated.")
    success_url = reverse_lazy('all_tasks')


class DeleteTaskView(PleaseLoginMixin, OwnerTestMixin, SuccessMessageMixin, DeleteView):
    """Класс-представление для удаления задачи."""

    model = Tasks
    pk_url_kwarg = 'task_id'
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('all_tasks')
    success_message = _("The task has been successfully deleted.")
    redirect_path = reverse_lazy("all_tasks")
    error_access_owner_message = _("A task can only be deleted by its author.")

    def get_owner(self):
        """Возвращает автора, т.е. владельца задачи."""
        return self.get_object().author


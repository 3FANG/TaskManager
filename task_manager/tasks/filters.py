import django_filters
from django.utils.translation import gettext_lazy as _
from django import forms

from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels


class TasksFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(queryset=Labels.objects.all())
    self_tasks = django_filters.BooleanFilter(label=_("Only your tasks"), method="get_user_tasks", widget=forms.CheckboxInput)

    def get_user_tasks(self, queryset, name, value):
        """Возвращает задачи только авторизованного пользователя."""
        # Если не указано значение, возвращаем переданный queryset
        if not value:
            return queryset
        return queryset.filter(author=self.request.user)

    class Meta:
        model = Tasks
        fields = ["status", "executor", "labels"]
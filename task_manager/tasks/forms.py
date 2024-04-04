from django import forms

from task_manager.tasks.models import Tasks, Statuses


class TaskCreationForm(forms.ModelForm):
    """Форма для создания задачи."""

    class Meta:
        model = Tasks
        fields = ["name", "description", "status", "executor"]


class FilterTasksForm(forms.ModelForm):
    """Форма для фильтрации задач."""

    # Переопределить status, чтобы это поле в форме было необязательным
    status = forms.ModelChoiceField(queryset=Statuses.objects.all(), required=False)

    class Meta:
        model = Tasks
        fields = ["status", "executor"]
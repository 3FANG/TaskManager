from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks, Statuses, Labels


class TaskCreationForm(forms.ModelForm):
    """Форма для создания задачи. Но ее также можно использовать и для ее обновления."""

    # Переопределил __init__, чтобы не создавать с нуля поле labels, а просто к уже существующему
    # добавить help_text
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].help_text = _("Press CTRL to select multiple labels.") # Зажмите CTRL, чтобы выбрать несколько меток

    class Meta:
        model = Tasks
        fields = ["name", "description", "status", "executor", "labels"]


class FilterTasksForm(forms.ModelForm):
    """Форма для фильтрации задач."""

    # Переопределяем status, чтобы это поле в форме было необязательным.
    # Также переопределяем labels, чтобы сделать выбор одной метки.
    # В противном случае, поле останется MultipleChoiceField
    status = forms.ModelChoiceField(queryset=Statuses.objects.all(), required=False)
    labels = forms.ModelChoiceField(queryset=Labels.objects.all(), required=False)

    class Meta:
        model = Tasks
        fields = ["status", "executor", "labels"]
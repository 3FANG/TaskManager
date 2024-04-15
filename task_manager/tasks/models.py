from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
from django.conf import settings

from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


# User = get_user_model()


class Tasks(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"))
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        verbose_name=_("status")
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("executor"),
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("author"),
        related_name=_("user_tasks")
    )
    labels = models.ManyToManyField(
        Labels,
        through="TasksLabels",
        verbose_name=_("labels"),
        blank=True
    )
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class TasksLabels(models.Model):
    """Промежуточная таблица отношения «многие ко многим» между задачами и метками."""

    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, verbose_name=_("task"))
    label = models.ForeignKey(Labels, on_delete=models.PROTECT, verbose_name=_("label"))

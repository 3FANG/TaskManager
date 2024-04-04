from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Statuses


User = get_user_model()


class Tasks(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"))
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, verbose_name=_("statuses"))
    executor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("executor"), null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("author"), related_name=_("user_tasks"))
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Statuses(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    date_created = models.DateTimeField(_("date created"), default=timezone.now)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name
from django.contrib import admin

from .models import Statuses


@admin.register(Statuses)
class StatusesAdmin(admin.ModelAdmin):
    pass

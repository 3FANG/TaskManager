from django.contrib import admin

from .models import Tasks, TasksLabels


class TasksLabelsInline(admin.TabularInline):
    model = TasksLabels


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    inlines = [
        TasksLabelsInline,
    ]

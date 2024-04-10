from django.contrib import admin

from .models import Labels


@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    pass

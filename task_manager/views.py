from django.shortcuts import render
from django.views import View


class HomePageView(View):
    """Класс-представление для домашней страницы."""

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

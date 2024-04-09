from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .fixtures import SetUpMixin


class TestCreateTask(SetUpMixin, TestCase):
    """Тестирование создания задачи."""

    def test_create_by_unauthorized_user(self):
        """Попытка создания задачи неавторизованным пользователем."""
        redirect_url = "/login/?next=/tasks/create/"
        route = reverse('create_task')
        response = self.client.get(route, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))
        response = self.client.post(route, data=self.create_form_data[0], follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))
        

    def test_create_by_authorized_user(self):
        """Создание задачи авторизованным пользователем."""
        route = reverse('create_task')
        template = 'tasks/create.html'
        self.client.login(username="1ONE", password="K3GauRS1")
        response = self.client.get(route)
        self.assertTemplateUsed(response, template)
        for data in self.create_form_data:
            with self.subTest("Ошибка создания задачи", form_data=data):
                response = self.client.post(route, data=data, follow=True)
                self.assertRedirects(response, reverse('all_tasks'))
                self.assertContains(response, _("The task has been successfully created."))
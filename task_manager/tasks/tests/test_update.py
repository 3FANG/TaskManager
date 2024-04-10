from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .fixtures import SetUpMixin


class TestUpdateTask(SetUpMixin, TestCase):
    """Тестирование обновления данных задачи."""

    def test_update_by_unauthorized_user(self):
        """Попытка обновить задачу неавторизованным пользователем."""
        route = reverse('update_task', args=[self.task.id])
        redirect_url = f'/login/?next=/tasks/{self.task.id}/update/'
        response = self.client.get(route, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))
        response = self.client.post(route, data=self.update_form_data[0], follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))

    def test_update_by_authorized_user(self):
        """Обновление задачи авторизованным пользователем."""
        route = reverse('update_task', args=[self.task.id])
        template = 'tasks/update.html'
        self.client.login(username="1ONE", password="K3GauRS1")
        response = self.client.get(route)
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)
        for data in self.update_form_data:
            with self.subTest("Ошибка обновления задачи", form_data=data):
                response = self.client.post(route, data=data, follow=True)
                self.assertRedirects(response, reverse('all_tasks'))
                self.assertContains(
                    response,
                    _("The task has been successfully updated.")
                )

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks
from .fixtures import SetUpMixin


class TestDeleteTask(SetUpMixin, TestCase):
    """Тестирование удаления задачи."""

    def test_delete_by_unauthorized_user(self):
        """Попытка удалить задачу неавторизованным пользователем."""
        route = reverse('delete_task', args=[self.task.id])
        redirect_url = f'/login/?next={route}'
        response = self.client.get(route, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))

    def test_delelete_by_authorized_user(self):
        """Удаление задачи авторизованным пользователем."""
        tasks_count = Tasks.objects.count()
        route = reverse('delete_task', args=[self.task.id])
        self.client.force_login(self.user_1)
        template = 'tasks/delete.html'
        response = self.client.get(route)
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_tasks'))
        self.assertEqual(Tasks.objects.count(), tasks_count - 1)
        self.assertContains(response, _("The task has been successfully deleted."))

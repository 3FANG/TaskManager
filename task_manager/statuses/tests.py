from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Statuses
from task_manager.tasks.models import Tasks
from task_manager.utils import get_message_text


User = get_user_model()


class TestCreateStatus(TestCase):
    """Тестирование создания статуса."""

    def setUp(self):
        """Создаем тестового пользователя и набор данных для отправки на POST запрос."""
        self.user = User.objects.create_user(username='auth')
        self.form_data = {
            'name': 'Status_1'
        }

    def test_create_by_unathorized_user(self):
        """Создание статуса неавторизованным пользователем."""
        redirect_url = '/login/?next=/statuses/create/'
        response = self.client.get(reverse('create_status'), follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(get_message_text(response), _("You are not logged in! Please log in."))
        response = self.client.post(reverse('create_status'), data=self.form_data, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(get_message_text(response), _("You are not logged in! Please log in."))

    def test_create_status(self):
        """Создание статуса авторизованным пользователем."""
        statuses_count = Statuses.objects.count()
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_status'), follow=True)
        self.assertTemplateUsed(response, 'statuses/create.html')
        response = self.client.post(reverse('create_status'), data=self.form_data, follow=True)
        self.assertRedirects(response, reverse('all_statuses'))
        self.assertEqual(get_message_text(response), _("Status successfully created."))
        self.assertEqual(Statuses.objects.count(), statuses_count + 1)


class TestReadStatuses(TestCase):
    """Тестирование просмотра статусов."""

    def setUp(self) -> None:
        """Создаем тестового пользователя."""
        self.user = User.objects.create_user(username='auth')

    def test_statuses_page_by_unauthorized(self):
        """Запрос неавторизованным пользователем пересылает на страницу авторизации."""
        route = reverse('all_statuses')
        redirect_url = '/login/?next=/statuses/'
        response = self.client.get(route, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(get_message_text(response), _("You are not logged in! Please log in.")) # Вы не авторизованы! Пожалуйста, выполните вход.

    def test_statuses_page_by_authorized(self):
        """Запрос авторизованным пользователем выводит страницу со статусами."""
        self.client.force_login(user=self.user)
        route = reverse('all_statuses')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        template = 'statuses/index.html'
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)

    
class TestUpdateStatus(TestCase):
    """Tестирование обновления данных статуса."""

    def setUp(self) -> None:
        """Создаем тестовые статусы и пользователя."""
        self.status_1 = Statuses.objects.create(name='status_1')
        self.status_2 = Statuses.objects.create(name='status_2')
        self.user = User.objects.create_user(username='auth')

    def test_update_by_unauthorized_user(self):
        """Попытка обновления данных статуса неавторизованным пользователем."""
        routes = {
            reverse('update_status', args=[self.status_1.id]): f"/login/?next=/statuses/{self.status_1.id}/update/",
            reverse('update_status', args=[self.status_2.id]): f"/login/?next=/statuses/{self.status_2.id}/update/",
        }
        for request_url, redirect_url in routes.items():
            with self.subTest(f"Ошибка перенаправления", redirect_url=redirect_url, request_url=request_url):
                response = self.client.get(request_url, follow=True)
                self.assertRedirects(response, expected_url=redirect_url)
                self.assertEqual(get_message_text(response), _("You are not logged in! Please log in.")) # Вы не авторизованы! Пожалуйста, выполните вход.

    def test_update_by_authorized_user(self):
        """Обновление данных статуса авторизованным пользователем."""
        routes = {
            reverse('update_status', args=[self.status_1.id]): self.status_1,
            reverse('update_status', args=[self.status_2.id]): self.status_2,
        }
        self.client.force_login(user=self.user)
        for route, status in routes.items():
            with self.subTest("Ошибка обновления статуса", route=route):
                response = self.client.get(route)
                self.assertTemplateUsed(response, 'statuses/update.html')
                response = self.client.post(route, data={'name': f"new_{status.name}"}, follow=True)
                self.assertRedirects(response, reverse('all_statuses'))
                self.assertEqual(get_message_text(response), _("Status has been successfully changed."))
                # Может сделать проверку, что статус действительно изменен, запросив новое название?


class TestDeleteStatus(TestCase):
    """Тестирование удаления статуса."""

    def setUp(self):
        """Создаем тестовые статусы и пользователя."""
        self.status_1 = Statuses.objects.create(name='status_1')
        self.status_2 = Statuses.objects.create(name='status_2')
        self.user = User.objects.create_user(username='auth')
        self.task_1 = Tasks.objects.create(
            name="Task",
            description="Description",
            status=self.status_1,
            executor=self.user,
            author=self.user
        )

    def test_delete_by_unauthorized_user(self):
        """Попытка удаления статуса неавторизованным пользователем."""
        routes = {
            reverse('delete_status', args=[self.status_1.id]): f"/login/?next=/statuses/{self.status_1.id}/delete/",
            reverse('delete_status', args=[self.status_2.id]): f"/login/?next=/statuses/{self.status_2.id}/delete/",
        }
        for request_url, redirect_url in routes.items():
            with self.subTest(f"Ошибка перенаправления", redirect_url=redirect_url, request_url=request_url):
                response = self.client.get(request_url, follow=True)
                self.assertRedirects(response, expected_url=redirect_url)
                self.assertEqual(get_message_text(response), _("You are not logged in! Please log in.")) # Вы не авторизованы! Пожалуйста, выполните вход.

    def test_delete_by_authorized_user_with_protected_instance(self):
        """Удаление статуса, связанного с задачами, авторизованным пользователем."""
        route = reverse('delete_status', args=[self.status_1.id])
        self.client.force_login(user=self.user)
        response = self.client.get(route)
        self.assertTemplateUsed(response, 'statuses/delete.html')
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_statuses'))
        self.assertEqual(get_message_text(response), _("You can't delete a status because it's associated with tasks."))
                
    def test_delete_by_authorized_user(self):
        """Удаление статуса, не связанного с задачами, авторизованным пользователем."""
        statuses_count = Statuses.objects.count()
        route = reverse('delete_status', args=[self.status_2.id])
        self.client.force_login(user=self.user)
        response = self.client.get(route)
        self.assertTemplateUsed(response, 'statuses/delete.html')
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_statuses'))
        self.assertEqual(Statuses.objects.count(), statuses_count - 1)
        self.assertEqual(get_message_text(response), _("Status has been successfully deleted."))
                


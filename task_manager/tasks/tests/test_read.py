from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Tasks, Labels
from .fixtures import SetUpMixin


class TestReadTasksList(SetUpMixin, TestCase):
    """Тестирование просмотра задач."""

    def setUp(self):
        super().setUp()
        self.label_1 = Labels.objects.create(name="Label1")
        self.label_2 = Labels.objects.create(name="Label2")

        self.task_1 = Tasks.objects.create(
            name="Task1",
            description="Description1",
            executor=self.user_2,
            status=self.status_1,
            author=self.user_1
        )
        self.task_1.save()
        self.task_1.labels.add(self.label_1)

        self.task_2 = Tasks.objects.create(
            name="Task2",
            description="Description2",
            executor=self.user_2,
            status=self.status_1,
            author=self.user_2
        )
        self.task_2.save()
        self.task_2.labels.add(self.label_1)

        self.task_3 = Tasks.objects.create(
            name="Task3",
            description="Description3",
            executor=self.user_2,
            status=self.status_2,
            author=self.user_1
        )
        self.task_3.save()
        self.task_3.labels.add(self.label_2)

    def test_tasks_page_by_unauthorized_user(self):
        """Запрос неавторизованным пользователем пересылает на страницу авторизации."""
        redirect_url_all_tasks = '/login/?next=/tasks/'
        response = self.client.get(reverse('all_tasks'), follow=True)
        self.assertRedirects(response, redirect_url_all_tasks)
        self.assertContains(response, _("You are not logged in! Please log in."))

    def test_tasks_page_by_authorized_user(self):
        """Запрос авторизованного пользователя возвращает страницу со всеми задачами."""
        route = reverse('all_tasks')
        template = 'tasks/index.html'
        self.client.force_login(self.user_1)
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)

    def test_filter_task_by_status(self):
        """Фильтрация задач по статусам."""
        required_tasks = Tasks.objects.filter(status=self.status_1)
        route = f"{reverse('all_tasks')}?status={self.status_1.id}"
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_message = f"Ожидаемый результат: {required_tasks}\n\
Полученный результат:{response.context['tasks_list']}"
        self.assertSetEqual(response.context['tasks_list'], required_tasks, error_message)

    def test_filter_task_by_executor(self):
        """Фильтрация задач по исполнителю."""
        route = f"{reverse('all_tasks')}?executor={self.user_1.id}"
        required_tasks = Tasks.objects.filter(executor=self.user_1)
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_message = f"Ожидаемый результат: {required_tasks}\n\
Полученный результат:{response.context['tasks_list']}"
        self.assertSetEqual(response.context['tasks_list'], required_tasks, error_message)

    def test_filter_task_by_labels(self):
        """Фильтрация задач по меткам"""
        route = f"{reverse('all_tasks')}?labels={self.label_1.id}"
        required_tasks = Tasks.objects.filter(labels=self.label_1)
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_message = f"Ожидаемый результат: {required_tasks}\n\
Полученный результат:{response.context['tasks_list']}"
        self.assertSetEqual(response.context['tasks_list'], required_tasks, error_message)

    def test_filter_only_your_tasks(self):
        """Вывод только своих задач."""
        route = f"{reverse('all_tasks')}?self_tasks=on"
        required_tasks = Tasks.objects.filter(author=self.user_1)
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_message = f"Ожидаемый результат: {required_tasks}\n\
Полученный результат:{response.context['tasks_list']}"
        self.assertSetEqual(response.context['tasks_list'], required_tasks, error_message)


class TestReadTask(SetUpMixin, TestCase):
    """Тестирование просмотра конкретной задачи."""

    def test_show_task_by_unauthorized_user(self):
        """Просмотр конкретной задачи неавторизованным пользователем."""
        redirect_url = f'/login/?next=/tasks/{self.task.id}/'
        response = self.client.get(reverse('show_task', args=[self.task.id]), follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))

    def test_show_task_by_authorized_user(self):
        """Просмотр конкретной задачи авторизованныйм пользователем."""
        route = reverse('show_task', args=[self.task.id])
        template = 'tasks/show.html'
        self.client.force_login(self.user_1)
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)

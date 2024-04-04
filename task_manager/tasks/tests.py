from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from task_manager.utils import get_message_text
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses


User = get_user_model()


class SetUpMixin:
    """Миксин, создающий все необходимые сущности и наборы данных."""
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username='1ONE',
            password='K3GauRS1'
        )
        self.user_2 = User.objects.create_user(
            username='DonUn',
            password='9o3rQaAc'
        )
        self.status_1 = Statuses.objects.create(name='Status1')
        self.status_2 = Statuses.objects.create(name='Status2')
        self.task = Tasks.objects.create(
            name="Task",
            description="Description",
            executor=self.user_2,
            status=self.status_1,
            author=self.user_1
        )
        self.create_form_data = [
            {
                "name": "Task1",
                "description": "Task_description1",
                "executor": self.user_2.id,
                "author": self.user_1.id,
                "status": self.status_1.id
            },
            {
                "name": "Task2",
                "description": "Task_description2",
                "executor": self.user_1.id,
                "author": self.user_1.id,
                "status": self.status_2.id
            },
            {
                "name": "Task3",
                "description": "Task_description3",
                "author": self.user_1.id,
                "status": self.status_1.id
            }
        ]
        self.update_form_data = [
            {
                "name": "New Task1",
                "description": "New Task_description1",
                "status": self.task.status.id,
                "executor": self.task.executor.id,
            },
            {
                "name": "New Task2",
                "description": "new_task_desc",
                "status": self.status_2.id,
                "executor": ''
            }
        ]


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


class TestReadTasks(SetUpMixin, TestCase):
    """Тестирование просмотра задач."""

    def test_tasks_page_by_unauthorized_user(self):
        """Запрос неавторизованным пользователем пересылает на страницу авторизации."""
        redirect_url_all_tasks = '/login/?next=/tasks/'
        redirect_url_show_task = f'/login/?next=/tasks/{self.task.id}/'
        response = self.client.get(reverse('all_tasks'), follow=True)
        self.assertRedirects(response, redirect_url_all_tasks)
        self.assertContains(response, _("You are not logged in! Please log in."))
        response = self.client.get(reverse('show_task', args=[self.task.id]), follow=True)
        self.assertRedirects(response, redirect_url_show_task)
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

    def test_show_task_by_authorized_user(self):
        """Просмотр конкретной задачи."""
        route = reverse('show_task', args=[self.task.id])
        template = 'tasks/show.html'
        self.client.force_login(self.user_1)
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)

        
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
                self.assertContains(response, _("The task has been successfully updated."))


class TestDeleteTask(SetUpMixin, TestCase):
    """Тестирование удаления задачи."""

    def test_delete_by_unauthorized_user(self):
        """Попытка удалить задачу неавторизованным пользователем."""
        route = reverse('delete_task', args=[self.task.id])
        redirect_url = f'/login/?next=/tasks/{self.task.id}/delete/' # можно ли использовать route?
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

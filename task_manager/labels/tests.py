from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message_text

from task_manager.tasks.models import Tasks, Labels, Statuses


User = get_user_model()


class SetUpMixin:
    """Миксин, создающий все необходимые сущности и наборы данных."""

    def setUp(self):
        self.form_data = {
            "name": "TestLabel"
        }
        self.user = User.objects.create_user(
            username='1ONE',
            password='K3GauRS1'
        )
        self.label_1 = Labels.objects.create(name="Label1")
        self.label_2 = Labels.objects.create(name="Label2")
        self.status = Statuses.objects.create(name="Status")
        self.task_1 = Tasks.objects.create(
            name="Task",
            description="Description",
            executor=self.user,
            status=self.status,
            author=self.user,
        )
        self.task_1.save()
        self.task_1.labels.add(self.label_1)


class TestCreateLabel(SetUpMixin, TestCase):
    """Тестирование создания метки."""

    def test_create_by_unauthorized_user(self):
        """Создание метки неавтотризованным пользователем."""
        redirect_url = '/login/?next=/labels/create/'
        response = self.client.get(reverse("create_label"), follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))
        response = self.client.post(reverse('create_label'), data=self.form_data, follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))


    def test_create_by_authorized_user(self):
        """Создание метки автотризованным пользователем."""
        labels_count = Labels.objects.count()
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_label'), follow=True)
        self.assertTemplateUsed(response, 'labels/create.html')
        response = self.client.post(reverse('create_label'), data=self.form_data, follow=True)
        self.assertRedirects(response, reverse('all_labels'))
        self.assertContains(response, _("Label successfully created."))
        self.assertEqual(Labels.objects.count(), labels_count + 1)


class TestReadLabels(SetUpMixin, TestCase):
    """Тестирование просмотра меток."""

    def test_labels_page_by_unauthorized(self):
        """Запрос неавторизованным пользователем пересылает на страницу авторизации."""
        redirect_url = '/login/?next=/labels/'
        response = self.client.get(reverse('all_labels'), follow=True)
        self.assertRedirects(response, redirect_url)
        self.assertContains(response, _("You are not logged in! Please log in."))

    def test_labels_page_by_authorized(self):
        """Запрос авторизованным пользователем выводит страницу с задачами."""
        self.client.force_login(user=self.user)
        route = reverse('all_labels')
        response = self.client.get(route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        template = 'labels/index.html'
        error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
        self.assertTemplateUsed(response, template, error_name)


class TestUpdateLabels(SetUpMixin, TestCase):
    """Тестирование обновления меток."""

    def test_update_by_unauthorized_user(self):
        """Попытка обновления данных метки неавторизованным пользователем."""
        routes = {
            reverse('update_label', args=[self.label_1.id]): f"/login/?next=/labels/{self.label_1.id}/update/",
            reverse('update_label', args=[self.label_2.id]): f"/login/?next=/labels/{self.label_2.id}/update/",
        }
        for request_url, redirect_url in routes.items():
            with self.subTest(f"Ошибка перенаправления", redirect_url=redirect_url, request_url=request_url):
                response = self.client.get(request_url, follow=True)
                self.assertRedirects(response, expected_url=redirect_url)
                self.assertContains(response, _("You are not logged in! Please log in."))

    def test_update_by_authorized_user(self):
        """Обновление данных метки авторизованным пользователем."""
        routes = {
            reverse('update_label', args=[self.label_1.id]): self.label_1,
            reverse('update_label', args=[self.label_2.id]): self.label_2,
        }
        self.client.force_login(user=self.user)
        for route, label in routes.items():
            with self.subTest("Ошибка обновления метки", route=route):
                response = self.client.get(route)
                self.assertTemplateUsed(response, 'labels/update.html')
                response = self.client.post(route, data={"name": f"New {label.name}"}, follow=True)
                self.assertRedirects(response, reverse('all_labels'))
                self.assertContains(response, _("Label has been successfully changed."))


class TestDeleteLabels(SetUpMixin, TestCase):
    """Тестирование удаления меток"""

    def test_delete_by_unauthorized_user(self):
        """Попытка удаления метки неавторизованным пользователем."""
        routes = {
            reverse('delete_label', args=[self.label_1.id]): f"/login/?next=/labels/{self.label_1.id}/delete/",
            reverse('delete_label', args=[self.label_1.id]): f"/login/?next=/labels/{self.label_1.id}/delete/",
        }
        for request_url, redirect_url in routes.items():
            with self.subTest(f"Ошибка перенаправления", redirect_url=redirect_url, request_url=request_url):
                response = self.client.get(request_url, follow=True)
                self.assertRedirects(response, redirect_url)
                self.assertContains(response, _("You are not logged in! Please log in."))

    def test_delete_by_authorized_user_with_protected_instance(self):
        """Удаление метки, связанной с задачами, авторизованным пользователем."""
        route = reverse('delete_label', args=[self.label_1.id])
        self.client.force_login(user=self.user)
        response = self.client.get(route)
        self.assertTemplateUsed(response, 'labels/delete.html')
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_labels'))
        # Почему не работае assertContains()?
        # self.assertContains(response, _("You can't delete a label because it's associated with tasks."))
        self.assertEqual(get_message_text(response), _("You can't delete a label because it's associated with tasks."))
                
    def test_delete_by_authorized_user(self):
        """Удаление метки, не связанной с задачами, авторизованным пользователем."""
        labels_count = Labels.objects.count()
        route = reverse('delete_label', args=[self.label_2.id])
        self.client.force_login(user=self.user)
        response = self.client.get(route)
        self.assertTemplateUsed(response, 'labels/delete.html')
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_labels'))
        self.assertEqual(Labels.objects.count(), labels_count - 1)
        self.assertContains(response, _("The label has been successfully removed."))
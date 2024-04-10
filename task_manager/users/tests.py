from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.utils import get_message_text
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses


User = get_user_model()


class TestCreateUser(TestCase):
    """Тестирование создания пользователя."""

    def test_create_user(self):
        """Валидная форма создает нового пользователя."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'username': '1ONE',
            'password1': 'K3GauRS1',
            'password2': 'K3GauRS1'
        }
        response = self.client.post(reverse('signup_user'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('login_user'))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(
            get_message_text(response),
            _("You have been successfully signed in.")
        )


class TestReadUser(TestCase):
    """Тестирование просмотра пользователей."""

    def test_users_page(self):
        """Страницы доступны по URL."""
        pages = (reverse('home'), reverse('all_users'))
        for page in pages:
            with self.subTest(f"Страница не доступна по адресу {page}"):
                error_name = f"Ошибка: нет доступа до страницы {page}"
                response = self.client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_correct_template(self):
        """Запрос возвращает ожидаемый шаблон."""
        templates_routes = {
            reverse('home'): 'base.html',
            reverse('all_users'): 'users/index.html'
        }
        for route, template in templates_routes.items():
            with self.subTest(f"Некорректный шаблон по адресу {route}"):
                error_name = f"Ошибка: маршрут {route} ожидал шаблон {template}"
                response = self.client.get(route)
                self.assertTemplateUsed(response, template, error_name)


class TestUpdateUser(TestCase):
    """Тестирование изменения данных пользователя."""

    def setUp(self) -> None:
        """Создаем двух тестовых пользователей."""
        self.test_user_1 = User.objects.create_user(
            username='1ONE',
            password='K3GauRS1'
        )
        self.test_user_2 = User.objects.create_user(
            username='DonUn',
            password='9o3rQaAc'
        )

    def test_redirect_unauthorized_user(self):
        """Редирект неавторизированного пользователя на страницу авторизации."""
        upd_user1_route = reverse('update_user', args=[self.test_user_1.id])
        upd_user2_route = reverse('update_user', args=[self.test_user_2.id])
        redirect_routes = {
            upd_user1_route: f"/login/?next={upd_user1_route}",
            upd_user2_route: f"/login/?next={upd_user2_route}",
        }
        for request_url, redirect_url in redirect_routes.items():
            with self.subTest(
                    "Ошибка перенаправления",
                    redirect_url=redirect_url,
                    request_url=request_url
                    ):
                response = self.client.get(request_url)
                self.assertRedirects(response, redirect_url)

    def test_updates_not_by_owner(self):
        """Изменения профиля не его владельцем."""
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(
            reverse('update_user', args=[self.test_user_2.id]),
            follow=True
        )
        self.assertRedirects(response, expected_url=reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("You don't have permissions to modify another user.")
        )
        response = self.client.post(
            reverse('update_user', args=[self.test_user_2.id]),
            data={
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'username',
            },
            follow=True
        )
        self.assertRedirects(response, expected_url=reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("You don't have permissions to modify another user.")
        )

    def test_updates_by_owner(self):
        """Изменения профиля его владельцем."""
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(
            reverse('update_user', args=[self.test_user_1.id]),
            follow=True
        )
        self.assertTemplateUsed(response, 'users/update.html')
        response = self.client.post(
            reverse('update_user', args=[self.test_user_1.id]),
            data={
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'username',
            },
            follow=True
        )
        self.assertRedirects(response, reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("The user data has been successfully changed.")
        )


class TestDeleteUser(TestCase):
    """Тестирование удаления пользователя."""

    def setUp(self) -> None:
        self.user_1 = User.objects.create_user(
            username='1ONE',
            password='K3GauRS1'
        )
        self.user_2 = User.objects.create_user(
            username='DonUn',
            password='9o3rQaAc'
        )
        self.status_1 = Statuses.objects.create(name="Status")
        self.task_1 = Tasks.objects.create(
            name="Task",
            description="Description",
            status=self.status_1,
            executor=self.user_1,
            author=self.user_1
        )

    def test_redirect_unauthorized_user(self):
        """Редирект неавторизированного пользователя на страницу авторизации."""
        del_user1_route = reverse('delete_user', args=[self.user_1.id])
        del_user2_route = reverse('delete_user', args=[self.user_2.id])
        redirect_routes = {
            del_user1_route: f"/login/?next={del_user1_route}",
            del_user2_route: f"/login/?next={del_user2_route}",
        }
        for request_url, redirect_url in redirect_routes.items():
            with self.subTest(
                    "Ошибка перенаправления",
                    redirect_url=redirect_url,
                    request_url=request_url
                    ):
                response = self.client.get(request_url)
                self.assertRedirects(response, redirect_url)

    def test_delete_not_by_owner(self):
        """Удаление профиля не его владельцем."""
        self.client.login(username='1ONE', password='K3GauRS1')
        response = self.client.get(
            reverse('delete_user', args=[self.user_2.id]),
            follow=True
        )
        self.assertRedirects(response, expected_url=reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("You do not have permissions to delete another user.")
        )
        response = self.client.post(
            reverse('delete_user', args=[self.user_2.id]),
            follow=True
        )
        self.assertRedirects(response, expected_url=reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("You do not have permissions to delete another user.")
        )

    def test_delete_by_owner_with_protected_instance(self):
        """Удаление профиля, у которого есть связанный задачи, его владельцем."""
        self.client.login(username='1ONE', password='K3GauRS1')
        route = reverse('delete_user', args=[self.user_1.id])
        response = self.client.get(route, follow=True)
        self.assertTemplateUsed(response, 'users/delete.html')
        response = self.client.post(route, follow=True)
        self.assertRedirects(response, reverse('all_users'))
        self.assertEqual(
            get_message_text(response),
            _("You can't delete a user because they are associated with tasks.")
        )

    def test_delete_by_owner(self):
        """Удаление профиля, у которого нет свяханных задач, его владельцем."""
        self.client.login(username='DonUn', password='9o3rQaAc')
        response = self.client.get(
            reverse('delete_user', args=[self.user_2.id]),
            follow=True
        )
        self.assertTemplateUsed(response, 'users/delete.html')
        response = self.client.post(
            reverse('delete_user', args=[self.user_2.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('all_users'))
        self.assertEqual(get_message_text(response), _("User successfully deleted."))

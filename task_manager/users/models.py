from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Переопределенная модель пользователя."""

    def __str__(self) -> str:
        return self.get_full_name()

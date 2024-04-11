from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """Переопределенная форма регистрации пользователя.
    
    Также это форма используется для изменения данных пользователя.
    Поля password1 и password2 не указывваются в field, т.к. этих полей
    нет в модели, они есть только в самой форме.
    """

    # UserCreationForm просит только username и password,
    # а мне нужен еще first_name и last_name
    # Также хочу изменить help_text у полей ввода

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

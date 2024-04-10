from django.contrib.messages import get_messages


def get_message_text(response) -> str:
    """Получить текст сообщения."""
    try:
        messages = list(get_messages(response.wsgi_request))
        return str(messages[0])
    # Если сообщение отсутствует
    except IndexError:
        return None

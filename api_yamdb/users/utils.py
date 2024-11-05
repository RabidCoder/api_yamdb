from random import randint
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .constants import CONFIRMATION_CODE_LENGTH

User = get_user_model()


def send_confirmation_code_to_email(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = ''.join([
        str(randint(0, 9)) for _ in range(CONFIRMATION_CODE_LENGTH)
    ])
    send_mail(
        subject='Код подтверждения для регистрации в проекте Yamdb',
        message=f'Для получения JWT-токена укажите код {confirmation_code}',
        from_email='admin@yamdb.ru',
        recipient_list=[user.email],
        fail_silently=False,
    )
    user.confirmation_code = confirmation_code
    user.save()

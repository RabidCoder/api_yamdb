from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api_yamdb.settings import ADMIN_EMAIL

User = get_user_model()


def send_confirmation_code_to_email(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения для регистрации в проекте Yamdb',
        message=f'Для получения JWT-токена укажите код {confirmation_code}',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    user.confirmation_code = confirmation_code
    user.save()

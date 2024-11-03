from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (USER, MODERATOR, ADMIN,
    CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
)
ROLE_CHOICE = [(USER, 'Пользователь'),
               (MODERATOR, 'Модератор'),
               (ADMIN, 'Администратор')
               ]

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length = MAX_USERNAME_LENGTH,
        unique = True,
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        blank=False
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICE,
        default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Проверочный код',
        blank=True,
        max_length=CONFIRMATION_CODE_LENGTH
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Информация о пользователе',
        default=''
    )


    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin'


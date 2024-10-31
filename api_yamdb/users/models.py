from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import CONFIRMATION_CODE_LENGTH, ROLE_CHOICE

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICE,
        default=ROLE_CHOICE[0]
        )
    confirmation_code = models.CharField(
        verbose_name='Проверочный код',
        blank=True,
        max_length=CONFIRMATION_CODE_LENGTH
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username


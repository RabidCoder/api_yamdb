from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ROLE_CHOICE

class CustomUser(AbstractUser):
    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICE,
        default=ROLE_CHOICE[0]
        )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username


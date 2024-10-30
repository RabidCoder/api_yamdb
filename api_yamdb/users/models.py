from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=15,
                            choices=[('user', 'Пользователь'),
                                     ('moderator', 'Модератор'),
                                     ('admin', 'Администратор')
                                     ]
                            )


    def __str__(self):
        return self.username
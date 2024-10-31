from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'role', 'email']
    list_display_links = ['username', 'email']
    list_editable = ['role']
    fieldsets = UserAdmin.fieldsets + (('Дополнительные поля:', {"fields": ["role"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Обязательные поля', {'fields': ['email', 'role']}),
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
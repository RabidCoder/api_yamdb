from re import fullmatch

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .constants import (BAD_USERNAMES, CONFIRMATION_CODE_LENGTH,
                        MAX_USERNAME_LENGTH, USERNAME_PATTERN)
from .permissions import IsAdminOrSuperuser

User = get_user_model()


class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value in BAD_USERNAMES or not fullmatch(USERNAME_PATTERN, value):
            raise serializers.ValidationError('Неправильное имя пользователя')
        return value


class GetTokenSerializers(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    permission_classes = (IsAdminOrSuperuser,)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value in BAD_USERNAMES or not fullmatch(USERNAME_PATTERN, value):
            raise serializers.ValidationError('Неправильное имя пользователя')
        return value

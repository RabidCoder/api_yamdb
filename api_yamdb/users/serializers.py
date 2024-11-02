from django.contrib.auth import get_user_model
from rest_framework import serializers

from .constants import MAX_USERNAME_LENGTH, CONFIRMATION_CODE_LENGTH

User = get_user_model()


class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializers(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True
    )

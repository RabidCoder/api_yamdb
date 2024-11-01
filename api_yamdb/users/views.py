from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .constants import BAD_USER_NAMES
from .serializers import SignUpSerializers
from .utils import send_confirmation_code_to_email

User=get_user_model()

def profile(request):
    return HttpResponse('<h1>Профиль пользователя</h1>')

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if not username or not email:
        return Response(
            {'email': 'email'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if username in BAD_USER_NAMES:
        return Response(
            {'error': f'Имя пользователя: {username} - не допустимо.'},
            status=status.HTTP_400_BAD_REQUEST
    )
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)

    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializers(user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        if user.email != serializer.validated_data['email']:
            return Response(
                {'error': f'Для пользователя {username} указана неправильная почта'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)




def get_token(request):
    pass
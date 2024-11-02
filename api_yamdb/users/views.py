from re import fullmatch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .constants import BAD_USERNAMES, USERNAME_PATTERN
from .serializers import SignUpSerializers, GetTokenSerializers
from .utils import send_confirmation_code_to_email

User=get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = GetTokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    #####
    Начать с этого
    #####
    username = request.data.get('username')
    email = request.data.get('email')
    answer = {}
    if not username:
        answer['username'] = ['Обязательное поле']
    if not email:
        answer['email'] = ['Обязательное поле']
    if answer:
        return Response(answer, status=status.HTTP_400_BAD_REQUEST)
    if username in BAD_USERNAMES or not fullmatch(USERNAME_PATTERN, username):
        return Response(
            {'username': [f'Неправильное имя пользователя: {username}'],
             'email': [f'или формат почтового адреса: {email}']},
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


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    confirmation_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code == confirmation_code:
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': [f'Проверочный код указан неправильно']},
        status=status.HTTP_400_BAD_REQUEST
    )


def blank_url(request):
    return HttpResponse('<h1>Заглушка</h1>')


def profile(request):
    return HttpResponse('<h1>Профиль пользователя</h1>')
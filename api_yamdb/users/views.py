from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


User=get_user_model()

def profile(request):
    return HttpResponse('<h1>Профиль пользователя</h1>')

def signup(request):
    if request.method != 'POST':
        return Response(
            'Для регистрации пользователя надо использовать метод "POST"',
            status=HTTP_400_BAD_REQUEST
        )


def get_token(request):
    pass
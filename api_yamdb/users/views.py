from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .constants import BAD_USER_NAMES
from .serializers import SignUpSerializers

User=get_user_model()

def profile(request):
    return HttpResponse('<h1>Профиль пользователя</h1>')

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if not username or not email:
        return Response(
            {'error': 'Проверьте, что в запросе присутствуют параметры username и email.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if username in BAD_USER_NAMES:
        return Response(
            {'error': f'Имя пользователя: {username} - не допустимо.'},
            status=status.HTTP_400_BAD_REQUEST
    )
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username)


    # if request.method != 'POST':
    #     return Response(
    #         {'message': 'Для регистрации пользователя надо использовать метод "POST"'},
    #         status=HTTP_400_BAD_REQUEST
    #     )
    #



def get_token(request):
    pass
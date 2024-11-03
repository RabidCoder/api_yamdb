from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import SignUpSerializers, GetTokenSerializers, UserSerializer
from .utils import send_confirmation_code_to_email

User=get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializers(data=request.data)
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user = get_object_or_404(User, username=username)
    email = request.data.get('email')
    if user.email != email:
        return Response(
            {'error': f'Для пользователя {username} указана неправильная почта'},
            status=status.HTTP_400_BAD_REQUEST
        )
    send_confirmation_code_to_email(username)
    return Response({}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
def create_user_by_admin(request):
    a = 1
    return HttpResponse('<h1>Создание пользователя администратором</h1>')


@api_view(['POST'])
def update_user_profile(request):
    return HttpResponse('<h1>Обновление данных профиля</h1>')


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAdminOrStaff,)
    # filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

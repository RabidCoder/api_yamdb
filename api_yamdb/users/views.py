from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrSuperuser
from .serializers import SignUpSerializers, GetTokenSerializers, UserSerializer
from .utils import send_confirmation_code_to_email

User = get_user_model()


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializers(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if user.email != serializer.validated_data['email']:
        return Response(
            {'username': ['Указана неправильная почта']},
            status=status.HTTP_400_BAD_REQUEST
        )
    send_confirmation_code_to_email(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username']
                             )
    confirmation_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code == confirmation_code:
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': ['Проверочный код указан неправильно']},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(IsAuthenticated,)
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

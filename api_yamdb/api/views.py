from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import AdminOrReadOnly
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (AdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

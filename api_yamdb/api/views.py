from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.mixins import ListCreateDestroyViewSet
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

from rest_framework import viewsets

from api.mixins import ListCreateDestroyViewSet
from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    pass

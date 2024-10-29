from api.mixins import ListCreateDestroyViewSet
from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class CategoryViewSet(ListCreateDestroyViewSet):
    model = Category
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    model = Genre
    serializer_class = GenreSerializer

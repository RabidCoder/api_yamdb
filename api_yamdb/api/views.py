from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import AdminOrReadOnly, AuthorOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReadTitleSerializer,
    ReviewSerializer,
    WriteTitleSerializer,
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Viewset class related to Categories.
    Inherits from api.mixins.ListCreateDestroyViewSet.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Viewset class related to Genres.
    Inherits from api.mixins.ListCreateDestroyViewSet.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset class related to Titles."""

    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Defines the Serializer to use in case of different actions."""
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return WriteTitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset class related to Comments."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset class related to Reviews."""

    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = self.get_title()
        user = self.request.user
        if Review.objects.filter(title=title, author=user).exists():
            raise ValidationError('You have already reviewed this title.')
        serializer.save(author=user, title=title)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

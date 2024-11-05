from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api import serializers
from api.filters import ReviewFilter, TitleFilter
from api.permissions import AdminPermission, CustomPermission
from reviews.models import Category, Genre, Review, Title


class BaseModelViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Base viewset that provides common functionality
    for category and genre viewsets.
    """

    permission_classes = (AdminPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class NonPutModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that extends ModelViewSet to customize the update method.
    """

    def update(self, request, *args, **kwargs):
        """
        Override the update method to block PUT requests.

        Returns a 405 Method Not Allowed response for PUT requests.
        """
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method "PUT" is not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)


class CategoryViewSet(BaseModelViewSet):
    """
    Viewset class related to Categories.

    Allows listing, creating, and deleting categories.
    """

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(BaseModelViewSet):
    """
    Viewset class related to Genres.

    Allows listing, creating, and deleting genres.
    """

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(NonPutModelViewSet):
    """Viewset class related to Titles."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        """Define the serializer to use for different actions."""
        if self.action in ('list', 'retrieve'):
            return serializers.ReadTitleSerializer
        return serializers.WriteTitleSerializer


class CommentViewSet(NonPutModelViewSet):
    """Viewset class related to Comments."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (CustomPermission,)

    def get_review(self):
        """Get the review object associated with the comment."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        """Save the comment with the associated review and the current user."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        """Get the queryset of comments related to a specific review."""
        review = self.get_review()
        return review.comments.all()


class ReviewViewSet(NonPutModelViewSet):
    """Viewset class related to Reviews."""

    serializer_class = serializers.ReviewSerializer
    permission_classes = (CustomPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReviewFilter

    def get_title(self):
        """Get the title object associated with the review."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        """Save the review with the associated title and the current user."""
        title = self.get_title()
        user = self.request.user
        if Review.objects.filter(title=title, author=user).exists():
            raise ValidationError(
                f'You have already reviewed this title "{title.name}".'
            )
        serializer.save(author=user, title=title)

    def get_queryset(self):
        """Get the queryset of reviews related to a specific title."""
        title = self.get_title()
        return title.reviews.all()

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from api import serializers
from api.filters import ReviewFilter, TitleFilter
from api.mixins import BaseModelViewSet, NonPutModelViewSet
from api.permissions import AdminPermission
from reviews.models import Category, Genre, Review, Title


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

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score')).order_by('-year', 'category', 'name')
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

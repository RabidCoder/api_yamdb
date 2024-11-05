import django_filters

from reviews.models import Review, Title


class ReviewFilter(django_filters.FilterSet):
    """Filter class related to Review model."""

    score = django_filters.NumberFilter(
        field_name='score',
        lookup_expr='exact'
    )
    author = django_filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains'
    )
    title = django_filters.CharFilter(
        field_name='title__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Review
        fields = ('score', 'author', 'title')


class TitleFilter(django_filters.FilterSet):
    """Filter class related to Title model."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')

from rest_framework import validators, serializers

from constants import MIN_SCORE, MAX_SCORE
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Serializer related to Category model."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Serializer related to Genre model."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class ReadTitleSerializer(serializers.ModelSerializer):
    """Serializer related to Title model read purpose."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class WriteTitleSerializer(serializers.ModelSerializer):
    """Serializer related to Title model write purpose."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('id', 'author', 'pub_date', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    comments = CommentSerializer(many=True, read_only=True)
    score = serializers.IntegerField(min_value=MIN_SCORE, max_value=MAX_SCORE)

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'score', 'author', 'pub_date', 'title', 'comments'
        )
        read_only_fields = ('id', 'author', 'pub_date', 'title', 'comments')

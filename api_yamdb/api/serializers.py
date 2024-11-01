from rest_framework import serializers

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

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('description',)


class WriteTitleSerializer(serializers.ModelSerializer):
    """Serializer related to Title model write purpose."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('description',)


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

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'score', 'author', 'pub_date', 'title', 'comments'
        )
        read_only_fields = ('id', 'author', 'pub_date', 'title', 'comments')

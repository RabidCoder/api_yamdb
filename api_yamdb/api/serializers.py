from rest_framework import serializers

from reviews.models import Category, Genre, Title, MIN_YEAR, current_year


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('description',)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate_year(self, value):
        if value < MIN_YEAR or value > current_year():
            raise serializers.ValidationError(
                'Invalid year! Correct range is (-20000...current_year).')
        return value

    def validate_category(self, category):
        if (
            not isinstance(category, str)
            or not Category.objects.filter(slug=category)
        ):
            raise serializers.ValidationError(
                f'Category slug string "{category}" does not exist!')
        return category

    def validate_genre(self, genres):
        if not isinstance(genres, list):
            raise serializers.ValidationError(
                'Genres must be a list!')
        for genre in genres:
            if (
                not isinstance(genre, str)
                or not Genre.objects.filter(slug=genre)
            ):
                raise serializers.ValidationError(
                    f'Genre slug string "{genre}" does not exist!')
        return genres

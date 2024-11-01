from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class BaseAdmin(admin.ModelAdmin):
    """Base class for common admin settings."""

    empty_value_display = '-empty-'
    list_display_links = ('name',)
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    search_fields = ('name', 'slug')


class ShortTextAdmin(BaseAdmin):
    """Extended base class to add short text functionality."""

    list_display_links = ('get_short_text',)

    def short_text(obj, field_name='text', length=50):
        """Returns a shortened version of the review or comment text."""
        text = getattr(obj, field_name, '')
        return text[:length] + '...' if len(text) > length else text

    def get_short_text(self, obj):
        return self.short_text(obj, 'text')

    get_short_text.short_description = 'Text Preview'


class CommentInline(admin.TabularInline):
    """Inline class for comments."""
    model = Comment
    extra = 1


class GenreInline(admin.TabularInline):
    """Inline class for genres."""

    model = Title.genre.through
    extra = 0


class ReviewInline(admin.TabularInline):
    """Inline class for reviews."""
    model = Review
    extra = 1


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """Admin settings for Category model."""

    pass


@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    """Admin settings for Genre model."""

    pass


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    """Admin settings for Title model."""

    inlines = (GenreInline, ReviewInline)
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'year', 'description', 'genre', 'category')
    list_filter = ('year', 'genre', 'category')


@admin.register(Comment)
class CommentAdmin(ShortTextAdmin):
    """Admin settings for Comment model."""

    list_display = ('get_short_text', 'author', 'pub_date')
    search_fields = ('text', 'author', 'review', 'pub_date')
    list_filter = ('review',)


@admin.register(Review)
class ReviewAdmin(ShortTextAdmin):
    """Admin settings for Review model."""

    inlines = (CommentInline,)
    list_display = ('get_short_text', 'score', 'author', 'pub_date')
    search_fields = ('text', 'score', 'author', 'title', 'pub_date')
    list_filter = ('title',)

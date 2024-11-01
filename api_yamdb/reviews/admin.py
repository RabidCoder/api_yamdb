from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


def short_text(obj, field_name='text', length=50):
    """Returns a shortened version of the review or comment text."""
    text = getattr(obj, field_name, '')
    return text[:length] + '...' if len(text) > length else text


class CommentInline(admin.TabularInline):
    """Class shows inline comments while administering reviews."""
    model = Comment
    extra = 1


class GenreInline(admin.TabularInline):
    """Class shows inline genres while administering titles."""

    model = Title.genre.through
    extra = 0


class ReviewInline(admin.TabularInline):
    """Class shows inline reviews while administering titles."""
    model = Review
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category administering customization form."""

    list_display = (
        'name',
        'slug',
    )
    list_editable = (
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_display_links = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre administering customization form."""

    list_display = (
        'name',
        'slug',
    )
    list_editable = (
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_display_links = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Title administering customization form."""

    inlines = (GenreInline, ReviewInline)
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = (
        'name',
        'year',
        'description',
        'genre',
        'category',
    )
    list_filter = (
        'year',
        'genre',
        'category',
    )
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment administering customization form."""

    list_display = (
        'text', 'author', 'pub_date'
    )
    search_fields = (
        'text', 'author', 'review', 'pub_date'
    )
    list_filter = ('review',)
    list_display_links = ('text',)
    empty_value_display = '-empty-'
    
    def get_short_text(self, obj):
        return short_text(obj, 'text')
    
    get_short_text.short_description = 'Comment'
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review administering customization form."""

    inlines = (CommentInline,)
    list_display = (
        'text', 'score', 'author', 'pub_date'
    )
    search_fields = (
        'text', 'score', 'author', 'title', 'pub_date'
    )
    list_filter = ('title',)
    list_display_links = ('text',)
    empty_value_display = '-empty-'

    def get_short_text(self, obj):
        return short_text(obj, 'text')
    
    get_short_text.short_description = 'Review'

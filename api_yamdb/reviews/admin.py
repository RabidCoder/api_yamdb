from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


def short_text(obj, field_name='text', length=50):
        """Возвращает сокращенную версию текста отзыва или комментария."""
        text = getattr(obj, field_name, '')
        return text[:length] + '...' if len(text) > length else text


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

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
    list_display = (
        'text', 'author', 'pub_date'
    )
    search_fields = (
        'text', 'author', 'review', 'pub_date'
    )
    list_filter = ('review',)
    list_display_links = ('text',)
    empty_value_display = '-пусто-'
    
    def get_short_text(self, obj):
        return short_text(obj, 'text')
    
    get_short_text.short_description = 'Comment'
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)
    list_display = (
        'text', 'score', 'author', 'pub_date'
    )
    search_fields = (
        'text', 'score', 'author', 'title', 'pub_date'
    )
    list_filter = ('title',)
    list_display_links = ('text',)
    empty_value_display = '-пусто-'

    def get_short_text(self, obj):
        return short_text(obj, 'text')
    
    get_short_text.short_description = 'Review'

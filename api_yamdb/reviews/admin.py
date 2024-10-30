from django.contrib import admin

from .models import Category, Genre, Title


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 0


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
    inlines = (GenreInline,)
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

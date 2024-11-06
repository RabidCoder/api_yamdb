import datetime

from django.core.validators import (
    MaxLengthValidator, MaxValueValidator, MinValueValidator
)
from django.db import models

from constants import (
    NAME_MAX_LENGTH, SLUG_MAX_LENGTH, MIN_YEAR, MIN_SCORE, MAX_SCORE
)
from users.models import CustomUser


def current_year():
    """Returns current year."""
    return datetime.date.today().year


class Category(models.Model):
    """Model related to categories."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH, unique=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH, unique=True, verbose_name='Слаг категории'
    )

    class Meta:
        ordering = ['slug', 'name']
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model related to genres."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH, unique=True, verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH, unique=True, verbose_name='Слаг жанра'
    )

    class Meta:
        ordering = ['slug', 'name']
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Model related to titles."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                current_year(), message='Year cannot be in the future.'
            ),
            MinValueValidator(MIN_YEAR)
        ],
        db_index=True,
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='titles', verbose_name='Жанры'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True,
        null=True, related_name='titles', verbose_name='Категория'
    )

    class Meta:
        ordering = ['-year', 'category', 'name']
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='unique_title_properties'
            ),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model related to reviews."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(500)], verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ['title', 'author']
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Review by {self.author} on {self.title}'


class Comment(models.Model):
    """Model related to comments."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        validators=[MaxLengthValidator(500)], verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'Comment by {self.author} on review {self.review}: '
            f'{self.text[:20]}...'
        )

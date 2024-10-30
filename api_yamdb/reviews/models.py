import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
MIN_YEAR = -20000
MIN_SCORE = 1
MAX_SCORE = 10


def current_year():
    return datetime.date.today().year


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ['slug', 'name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ['slug', 'name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(current_year()),
            MinValueValidator(MIN_YEAR)
        ]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ['-year', 'category', 'name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ['title', 'author']
        verbose_name = 'Отзыв.'
        verbose_name_plural = 'Отзывы.'
    
    def __str__(self):
        return f'Отзыв пользователя {self.author} на произведение {self.title}'


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий.'
        verbose_name_plural = 'Комментарии.'
    
    def __str__(self):
        return f'Комментарий пользователя {self.author} на отзыв {self.review}'

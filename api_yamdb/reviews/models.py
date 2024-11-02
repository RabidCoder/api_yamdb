import datetime

from django.core.validators import (
    MaxValueValidator, MinValueValidator, MaxLengthValidator
)
from django.db import models

from users.models import CustomUser


NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
MIN_YEAR = -20000
MIN_SCORE = 1
MAX_SCORE = 10


def current_year():
    """Returns current year."""
    return datetime.date.today().year


class Category(models.Model):
    """Model related to categories."""

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ['slug', 'name']
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model related to genres."""

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ['slug', 'name']
        verbose_name = 'genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Model related to titles."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                current_year(), message='Year cannot be in the future.'
            ),
            MinValueValidator(MIN_YEAR)
        ]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='titles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True,
        null=True, related_name='titles'
    )

    class Meta:
        ordering = ['-year', 'category', 'name']
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
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(validators=[MaxLengthValidator(500)])
    score = models.IntegerField(
        validators=[MaxValueValidator(MAX_SCORE), MinValueValidator(MIN_SCORE)]
    )
    pub_date = models.DateTimeField(
        'Publication Date', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ['title', 'author']
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'Review by {self.author} on {self.title}'


class Comment(models.Model):
    """Model related to comments."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(validators=[MaxLengthValidator(500)])
    pub_date = models.DateTimeField(
        'Publication Date', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return (
            f'Comment by {self.author} on review {self.review}: '
            f'{self.text[:20]}...'
        )

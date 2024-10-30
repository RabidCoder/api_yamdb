import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
MIN_YEAR = -20000


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

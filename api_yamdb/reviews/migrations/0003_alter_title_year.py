# Generated by Django 3.2 on 2024-11-06 08:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, validators=[django.core.validators.MaxValueValidator(2024, message='Year cannot be in the future.'), django.core.validators.MinValueValidator(100)]),
        ),
    ]

# Generated by Django 3.2 on 2024-10-30 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20241029_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, to='reviews.Genre'),
        ),
    ]
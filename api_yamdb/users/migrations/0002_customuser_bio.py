# Generated by Django 3.2 on 2024-10-31 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(null=True, verbose_name='Биография'),
        ),
    ]

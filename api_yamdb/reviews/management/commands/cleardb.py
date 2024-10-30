from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Title_Genre

DATA = (Category, Genre, Title, Title_Genre)


class Command(BaseCommand):
    help = 'Clears tables in a database.'

    def handle(self, *args, **options):
        for table in DATA:
            records = table.objects.all()
            records.delete()
            print(f'{table} flush complete!')
        print('Done!')

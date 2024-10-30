from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title

DATA = (Category, Genre, Title)


class Command(BaseCommand):
    help = 'Clears tables in a database.'

    def handle(self, *args, **options):
        for table in DATA:
            records = table.objects.all()
            records.delete()
            print(f'{table} flush complete!')
        print('Done!')

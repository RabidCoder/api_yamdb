import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title


DIR = 'static/data/'

ROWDATA = {
    Category: 'category.csv',
    Genre: 'genre.csv',
}

TITLEDATA = (Title, 'titles.csv')

TITLEGENREDATA = (Title, 'genre_title.csv')


class Command(BaseCommand):
    help = 'Imports data from CSV file into the sqlite table.'

    def handle(self, *args, **options):

        for table, src in ROWDATA.items():
            with open(f'{DIR}{src}', 'r', encoding='utf-8') as datafile:
                reader = csv.DictReader(datafile)
                table.objects.bulk_create(
                    (table(**row) for row in reader),
                    ignore_conflicts=True
                )
                print(f'{table} data import complete!')

        table, src = TITLEDATA
        with open(f'{DIR}{src}', 'r', encoding='utf-8') as datafile:
            reader = csv.DictReader(datafile)
            for row in reader:
                table.objects.create(
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category'])
                )
            print(f'{table} data import complete!')
        print('Done!')

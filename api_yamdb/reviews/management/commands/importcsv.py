from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine


DIR = 'static/data/'

DATA = {
    'reviews_category': 'category.csv',
    'reviews_genre': 'genre.csv',
    'reviews_title': 'titles.csv',
    'reviews_title_genre': 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Imports data from CSV file into the sqlite table.'

    def handle(self, *args, **options):
        engine = create_engine('sqlite:///db.sqlite3')
        for table_name, csv_name in DATA.items():
            df = pd.read_csv(f'{DIR}{csv_name}')
            df.to_sql(table_name, engine, index=False, if_exists='replace')
            print(f'Table {table_name} complete!')
        print('Done!')

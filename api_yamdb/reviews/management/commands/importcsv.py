from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine


DB = 'sqlite:///db.sqlite3'

DIR = 'static/data/'

DATA = {
    'reviews_category': 'category.csv',
    'reviews_genre': 'genre.csv',
    'reviews_title': 'titles.csv',
    'reviews_title_genre': 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Imports data from CSV files into sqlite tables.'

    def handle(self, *args, **options):
        engine = create_engine(DB)
        for table_name, csv_name in DATA.items():
            df = pd.read_csv(f'{DIR}{csv_name}')
            df.to_sql(table_name, engine, index=False, if_exists='append')
            print(f'Table {table_name}: data import complete!')
        print('================================================\nDone!')

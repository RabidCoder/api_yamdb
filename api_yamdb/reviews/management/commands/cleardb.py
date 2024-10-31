from django.core.management.base import BaseCommand
from sqlalchemy import create_engine, text


DB = 'sqlite:///db.sqlite3'

TABLES = (
    'reviews_category',
    'reviews_genre',
    'reviews_title',
    'reviews_title_genre',
)


class Command(BaseCommand):
    help = 'Clears sqlite tables.'

    def handle(self, *args, **options):
        engine = create_engine(DB)
        for table_name in TABLES:
            with engine.begin() as conn:
                conn.execute(text(f'DELETE FROM {table_name}'))
            print(f'Table {table_name}: flush complete!')
        print('================================================\nDone!')

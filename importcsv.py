import pandas as pd
from sqlalchemy import create_engine


DB = 'sqlite:///api_yamdb/db.sqlite3'

DIR = 'api_yamdb/static/data/'

DATA = {
    'reviews_category': 'category.csv',
    'reviews_genre': 'genre.csv',
    'reviews_title': 'titles.csv',
    'reviews_title_genre': 'genre_title.csv',
    'reviews_comment': 'comments.csv',
    'reviews_review': 'review.csv',
    'users_customuser': 'users.csv',
}


def main():
    engine = create_engine(DB)
    for table_name, csv_name in DATA.items():
        df = pd.read_csv(f'{DIR}{csv_name}')
        df.to_sql(table_name, engine, index=False, if_exists='append')
        print(f'Table {table_name}: data import complete!')
    print('================================================\nDone!')


if __name__ == '__main__':
    main()

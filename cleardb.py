from sqlalchemy import create_engine, text


DB = 'sqlite:///api_yamdb/db.sqlite3'

TABLES = (
    'reviews_category',
    'reviews_genre',
    'reviews_title',
    'reviews_title_genre',
    'reviews_comment',
    'reviews_review',
    'users_customuser'
)


def main():
    engine = create_engine(DB)
    for table_name in TABLES:
        with engine.begin() as conn:
            conn.execute(text(f'DELETE FROM {table_name}'))
        print(f'Table {table_name}: flush complete!')
    print('================================================\nDone!')


if __name__ == '__main__':
    main()

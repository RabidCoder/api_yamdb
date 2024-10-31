### Описание проекта:

Проект реализует API для портала отзывов на произведения искусства. Выполнен на django rest framework.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:RabidCoder/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Как работать с проектом:

Документация к API после запуска приложения доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```

Примеры запросов к API доступны в корневом файле
```
api-requests.http
```
а также в коллекции для Postman в каталоге
```
postman_collection/
```

### Как загрузить тестовые данные в базу данных проекта:
```
python3 importcsv.py
```
### Как очистить базу данных проекта от тестовых данных:
```
python3 cleardb.py
```
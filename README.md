# YaMDb

Учебный проект Яндекс.Практикум курса Python-разработчик(backend).

## Описание:

YaMDb - база данных, которая собирает отзывы о различных произведениях. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». При необходимости, список категорий может быть расширен администратором. Пользователи могут оставлять рецензии на произведения и ставить оценки.

Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.

## Как запустить проект:

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

## Документация к API

 После запуска dev-сервера документация к API доступна по адресу:
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

## Как загрузить тестовые данные в базу данных проекта:
```
python3 importcsv.py
```
## Как очистить базу данных проекта от тестовых данных:
```
python3 cleardb.py
```

## Авторы

 Александр Кречетов (krechet0v.alex@yandex.ru)
 
 Александр Ролдугин (alexander@roldug.in)
 
 Владислав Васильев (vladen21@yandex.ru)
 

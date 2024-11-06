CONFIRMATION_CODE_LENGTH = 6
MAX_EMAIL_LENGTH = 254
MAX_USERNAME_LENGTH = 150
NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50

MIN_YEAR = 100

MIN_SCORE = 1
MAX_SCORE = 10

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

BAD_USERNAMES = ['me']
USERNAME_PATTERN = r'^[\w.@+-]+\Z'


ROLE_CHOICE = [
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь')
]

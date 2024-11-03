# ROLE_CHOICE = [('user', 'Пользователь'),
#                ('moderator', 'Модератор'),
#                ('admin', 'Администратор')
#                ]
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USERNAME_PATTERN = r'^[\w.@+-]+\Z'
BAD_USERNAMES = ['me']

CONFIRMATION_CODE_LENGTH = 6
MAX_EMAIL_LENGTH = 254
MAX_USERNAME_LENGTH = 150

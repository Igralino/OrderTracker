import os
import random

rand = random.SystemRandom()


def get_random_key(length=50):
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(characters) for _ in range(length))


CSRF_ENABLED = True
SECRET_KEY = get_random_key()
SECURITY_PASSWORD_SALT = 'my_precious_two'
basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'my_precious'
SECURITY_PASSWORD_SALT = 'my_precious_two'

MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'no_reply@mshp.yaconnect.com'
MAIL_PASSWORD = 'qwertyuiop1234567890'

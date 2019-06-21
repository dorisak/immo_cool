from .base import *
from os import environ


SECRET_KEY = os.getenv("IMMOCOOL_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ['104.248.136.26']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("IMMOCOOL_DB_NAME"),
        'USER': os.getenv('IMMOCOOL_DB_USER'),
        'PASSWORD': os.getenv('IMMOCOOL_DB_PWD'),
        'HOST': '',
        'PORT': '5432',
    }
}

ADMINS = os.getenv('IMMOCOOL_ADMNS')
EMAIL_HOST = os.getenv('IMMOCOOL_EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('IMMOCOOL_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('IMMOCOOL_EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('IMMOCOOL_EMAIL_PORT')

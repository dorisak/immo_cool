from . import *
import os

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['104.248.136.26']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PWD'],
        'HOST': '',
        'PORT': '5432',
    }
}

ADMINS = os.environ['ADMNS']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']

import os
from .base import *
from decouple import config

if 'TRAVIS' in os.environ:

    SECRET_KEY = config('SECRET_KEY')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '127.0.0.1/32',
            'PORT': '5433',
        },
    }

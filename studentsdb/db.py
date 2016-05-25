__author__ = 'berluskuni'
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Database

DATABASES = {
    # 'default': {
    #    'ENGINE': 'django.db.backend.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, '..', db.sqlite3)
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'students_db_user',
        'PASSWORD': '0503613075',
        'NAME': 'students_db',
    }
}


"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'USER': 'students_db_user',
        'PASSWORD': '0503613075',
        'NAME': 'studentsdb',
        'PORT': '',
    }
}
"""
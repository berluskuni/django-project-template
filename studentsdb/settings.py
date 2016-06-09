# coding=utf-8
"""
Django settings for studentsdb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*w)k_fcvn!jl1(%yv#b&&sh#v1$!ewj!8u%*sv&#0l52mi!cko'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'registration',
    'social.apps.django_app.default',
    'students',
    'studentsdb',
    # 'contact_form',
)

MIDDLEWARE_CLASSES = (
    'studentsdb.middleware.RequestTimeMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        "django.core.context_processors.request",
        'social.apps.django_app.context_processors.backends',
        "social.apps.django_app.context_processors.login_redirect",
        "studentsdb.context_processors.students_proc",
        "students.context_processors.group_processor",

    )
)

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1830631860498005'
SOCIAL_AUTH_FACEBOOK_SECRET = '5b2ad8fb372c5288d46eb36457bbfcb1'


CRISPY_TEMPLATE_PACK = 'bootstrap3'

PORTAL_URL = 'http://localhost:8000'

ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'

from .db import DATABASES
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.expanduser('~'),
                           '/home/berluskuni/Virtualenvs/studentsdb/src/studentsdb/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),

)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = os.path.join(BASE_DIR, "..", 'media')

MEDIA_URL = '/media/'

VALID_IMAGE_FORMATS = ('image/bmp', 'image/jpeg', 'image/gif', 'image/png',)

# для работы формы обратной связи
ADMIN_EMAIL = 'berluskuni@mail.ru'
EMAIL_USE_TLS = False
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'berluskuni@mail.ru'
EMAIL_HOST_PASSWORD = 'ganzhik7897770'
# end

# Налоштовуємо логери для нашего сайта
LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disables_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        "simple": {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'students.views.contact_admin': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}

REGISTRATION_OPEN = True

LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'
import os
from pathlib import Path
import cloudinary as cloudinary
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-o*ill^lq3+@((rn$3&=%askptlr7szcg&-mhq8)244gg6%)bjq'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookstore.accounts',
    'bookstore.profiles',
    'bookstore.books',
    'bookstore.news',
    'rest_framework',
    'bookstore.api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bookstore.error_handler.ErrorHandlerMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'bookstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd9ga73gkjasaso',
        'USER': 'usvxvkldvxojue',
        'PASSWORD': '381aa37d8dc7eb70a510fb0cc0cf53f7c70c68bf7ff26df94b1ea2dc4c7934a6',
        'HOST': 'ec2-52-18-116-67.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# MEDIA_URL = '/media/'
#
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.BookstoreUser'

LOGIN_URL = '/signup/'

# Decided to use cloudinary instead of metia files.
cloudinary.config(
    cloud_name='dmg3yiqqp',
    api_key='992435269518352',
    api_secret='6AftnY2bnBzJ_9TwFjOpLCJUJns'
)

CELERY_BROKER_URL = 'rediss://:p4e0cee314e2c8d927ce8b4fdaf157ec2e54780c68fa0fb5268c1d3a3ef0b2dae@ec2-46-137-29-65.eu-west-1.compute.amazonaws.com:9160'
# CELERY_RESULT_BACKEND = config('CELERY_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mailserverWE@gmail.com'
EMAIL_HOST_PASSWORD = 'ketzmihtzvqhnzsq'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# django-admin makemessages -l bg
# django-admin compilemessages

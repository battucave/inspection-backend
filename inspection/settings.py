"""
Django settings for inspection project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import datetime
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if not DEBUG:
    SECRET_KEY = config('SECRET_KEY')
else:
    SECRET_KEY = 'KJHBNbVjnvHBIbJBIjVBkjbKJBJbnjHGXTFXGFxtTF'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'property',
    'authapp',
    'rest_framework',
    'djoser',
    'report',
    'emergency',
    'mrequest',
    'messaging',
    'drf_yasg',
    'channels'    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inspection.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'inspection.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# if not DEBUG:
#     DATABASES = {
#         'default': {

#             'ENGINE': 'django.db.backends.postgresql_psycopg2',

#             'NAME': 'hospital',

#             'USER': 'postgresconfa',

#             'PASSWORD': 'postgres12#$',

#             'HOST': '127.0.0.1',

#             'PORT': '5432',

#         }

#     }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',

 
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FIXTURE_DIRS = (
    BASE_DIR / 'fixtures',
    )

AUTH_USER_MODEL = 'authapp.User'
#AUTHENTICATION_BACKENDS = ('authapp.backends.EmailBackend')
#configure DRF

#'DEFAULT_FILTER_BACKENDS': [
#        'django_filters.rest_framework.DjangoFilterBackend'
#    ],
REST_FRAMEWORK = {
 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework_simplejwt.authentication.JWTAuthentication',
    
    ),
    'DEFAULT_SCHEMA_CLASS':   'rest_framework.schemas.coreapi.AutoSchema',
   
}



SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Base url to serve media files
MEDIA_URL = 'http://127.0.0.1:8000/'

# Path where media is stored
MEDIA_ROOT =  BASE_DIR / 'media'

if not DEBUG:
    SENDGRID_API_KEY = config('SENDGRID_API_KEY')
else:
    SENDGRID_API_KEY = 'YOUR_API_KEY'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DJOSER={
'SEND_ACTIVATION_EMAIL': False,
'SERIALIZERS':{
    'user':'authapp.serializers.UserCreateSerializer',
    'current_user':'authapp.serializers.UserCreateSerializer'
}
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(weeks=1),
    "TOKEN_OBTAIN_SERIALIZER": "authapp.views.TokenObtainPairSerializer",
}





if not DEBUG:
    STATIC_ROOT = '/home/ubuntu/static'
    MEDIA_ROOT= '/home/ubuntu/media'
    MEDIA_URL = 'http://35.178.202.49/media/'

#STATIC_ROOT = '/home/ubuntu/static'
#MEDIA_ROOT= '/home/ubuntu/media'

# Channels
ASGI_APPLICATION = 'inspection.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
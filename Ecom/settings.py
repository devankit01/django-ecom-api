from datetime import timedelta
import os
from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY',"Nothing we are geting from the .env file.")
print(SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'EcomAPI',
    'django_filters',
    'django_crontab',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'EcomAPI.custom_middleware.simple_middleware'
]

ROOT_URLCONF = 'Ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'EcomAPI.context_process.first_context_process'
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
    },
    'default12': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':config('NAME') ,
        'USER':config('USER'),
        'PASSWORD':config('PASSWORD'),
        'HOST': 'raja.db.elephantsql.com',
        'PORT': '5432',
    },
    'users_db':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('NAME_USERDB') ,
        'USER': config('USER_USERDB'),
        'PASSWORD': config('PASSWORD_USERDB'),
        'HOST': 'batyr.db.elephantsql.com',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEBUG = True  # False For PRODUCTION


STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_S3_ENDPOINT_URL =config('AWS_S3_ENDPOINT_URL')
DEFAULT_FILE_STORAGE =config('DEFAULT_FILE_STORAGE')
AWS_S3_REGION_NAME =config('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID_S3 =config('AWS_ACCESS_KEY_ID_S3')
AWS_SECRET_ACCESS_KEY_S3 =config('AWS_SECRET_ACCESS_KEY_S3')
AWS_STORAGE_BUCKET_NAME =config('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL =config('AWS_DEFAULT_ACL')


# JWT Include
REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}


# Fetching email credentials from .env file
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'SIGNING_KEY': SECRET_KEY,

}

# Variable from env for AWS Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')
BUCKET_NAME = config('BUCKET_NAME')
# SNS SENDER ID
SENDER_ID = config('SENDER_ID')

#OTP TIME OUT
OTP_TIME_OUT = config('OTP_TIME_OUT')




# Logger Settings
DEBUG_FILE = os.path.join(BASE_DIR,"Logs/app.log")

LOGGING = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "%(asctime)s,%(levelname)s,%(module)s,%(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'per_day_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': DEBUG_FILE,
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 30, # how many backup file to keep, 30 days
            'formatter': 'verbose',
        }        
    },
    'loggers': {
        'django': {
            'handlers': ['per_day_file'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1  # 60 minutes
# Configuration of multiple database by router
DATABASE_ROUTERS=['routers.db_routers.AuthRouter']


CRONJOBS = [
    ('00 05 * * *', 'Logs.uploadLogs.logUpload'),  # for running cron everyday
    """
    python3 manage.py crontab add -> to add new cron job
    python3 manage.py crontab show -> to show existing cron job
    python3 manage.py crontab delete -> to delete cron job
    python3 manage.py crontab run 'cron id' -> to run specific cron job
    """
]
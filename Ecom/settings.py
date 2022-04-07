from datetime import timedelta
import os
from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '52wn%at)_xjuw%dv%-9y9x!rlieo6^l8oo%&cygy9)2*%@_x5u'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nlgrjmua',
        'USER': 'nlgrjmua',
        'PASSWORD': 'HOyW_TsmgdR-U9Nyx1v4BdUCxTteKu-n',
        'HOST': 'raja.db.elephantsql.com',
        'PORT': '5432',
    }
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

DEBUG = False  # For PRODUCTION


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

AWS_S3_ENDPOINT_URL = 'https://s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_ACCESS_KEY_ID = 'AKIAXLSZRNQVOCBWCHDU'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'serverless-django3'
AWS_DEFAULT_ACL = None


# JWT Include
REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no.reply.django3@gmail.com'
EMAIL_HOST_PASSWORD = 'Ankit@98'

# in-v3.mailjet.com, 587, key : f64a2dfbd9e4eb6fcb59e8977356a715, pass : 3afb6e941bc1ae7fc5e905331221dd8c
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'SIGNING_KEY': SECRET_KEY,

}

# Variable from env for AWS Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')
# SNS SENDER ID
SENDER_ID = config('SENDER_ID')



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
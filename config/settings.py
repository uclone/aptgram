"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# for Heroku
#import dj_database_url

# for Amazon & Mysql
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '47z6b0hi+&twg!)y&-vrzmue=cf#+y_tmjb2)!t5*_%(4er+)c'


# SECURITY WARNING: don't run with debug turned on in production! ---------------Amazon Server AWS EC2
#DEBUG = False
#ALLOWED_HOSTS = ['.compute.amazonaws.com']                       #---------------Amazon Server AWS EC2
# for Heroku
DEBUG = False
ALLOWED_HOSTS = ['*']                       #---------------remote server
# for Local
#DEBUG = True
#ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'filegram',
    'accounts',
    'storages',
    'resident',
    'sulbigram',
    'jumingram',
    'taskgram',
    'equipgram',
    'plangram',
    'lifegram',
    'crispy_forms',
    'index',
    'metergram',
    'papergram',
    'susungram',
    'bootstrap3',
    'bootstrap_datepicker_plus',
    'timegram',
    'newsgram',
    'django.contrib.humanize',
    'introgram',
    'pollgram',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',                   # for Heroku
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#for Local Database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

#for Heroku Database
#DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

#for Amazon Database aptgram
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aptgram',
        'USER': 'admin',
        'PASSWORD': '3457amazon',
        'HOST': 'aptgram.cexvtitcxxdk.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',

        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO'"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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

def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS['VERBOSE_LOOKUPS'].copy()
    verbose_lookups.update({
        'exact': '(완전 일치)',
        'icontains': '(일부 포함)',
        'contains': '(일부 포함)',
        'range': '(2020-01-01, 2020-12-12)',
    })
    return verbose_lookups

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ko-kr'

DATE_INPUT_FORMATS = ['%Y-%m-%d']

TIME_ZONE = 'Asia/Seoul'
#USE_TZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True

#for login
LOGIN_REDIRECT_URL = '/index/'

#for Crispy
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Media files (files, photos)
# for localhost storage -- linked to "config/url.py -- the last line"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# for Amazon -- Bucket - Aptgram
AWS_ACCESS_KEY_ID = 'AKIAWYGKWKC7DYLERDFG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'aptgram'
AWS_DEFAULT_ACL = None                                                      # by Warning by leebc
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'config.asset_storage.MediaStorage'                  #media

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# Default
#STATIC_URL = '/static/'
# for Herku
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')                         # for Heroku, Pythonanywhere

# for Amazon -- Static under Bucket
AWS_DEFAULT_ACL = 'public-read'                                             #shopping
AWS_LOCATION = 'static'                                                     #shopping
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)        #shopping
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'            #shopping



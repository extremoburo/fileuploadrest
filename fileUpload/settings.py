"""
Django settings for fileUpload project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's#3e8v2rh-q&+)$hg^0j7s_(%4slfgcnif&7ba!lf1_t#qxmr9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

"""
From: https://docs.djangoproject.com/en/1.11/ref/models/fields/
In your settings file, you’ll need to define MEDIA_ROOT as the full path to a
directory where you’d like Django to store uploaded files. (For performance,
these files are not stored in the database.) Define MEDIA_URL as the base
public URL of that directory.
Make sure that this directory is writable by the Web server’s user account.
"""

# Path to store images

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ************************************************************************
# http://django-minio-storage.readthedocs.io/en/latest/usage/
# BEGIN: django-minio-storage's settings
# ************************************************************************

# The access URL for the service
MINIO_STORAGE_ENDPOINT = "localhost:9000"
# Credentials
MINIO_STORAGE_ACCESS_KEY = "R0PNIYVHOJ1L6HJ4NXXG"
MINIO_STORAGE_SECRET_KEY = "Fs1MtBj4j0e4PXMepLleh9rwySJzB9eavbaSPkcS"
# Whether to use TLS or not (default: True)
MINIO_STORAGE_USE_HTTPS = False
# The bucket that will act as MEDIA folder
MINIO_STORAGE_MEDIA_BUCKET_NAME = "mediabucket"
# Whether to create the bucket if it does not already exist (default: False)
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
# The bucket that will act as STATIC folder
MINIO_STORAGE_STATIC_BUCKET_NAME = "staticbucket"
# Whether to create the bucket if it does not already exist (default: False)
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
# The base URL for generating urls to objects from  MinioMediaStorage
MINIO_STORAGE_MEDIA_URL = None
# The base URL for generating URLs to objects from MinioStaticStorage
MINIO_STORAGE_STATIC_URL = None
# Determines if the media file URLs should be pre-signed (default: False)
MINIO_STORAGE_MEDIA_USE_PRESIGNED = False
# Determines if the static file URLs should be pre-signed (default: False)
MINIO_STORAGE_STATIC_USE_PRESIGNED = False

# ************************************************************************
# END: django-minio-storage's settings
# ************************************************************************

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # PROJECT APPS
    'fileUpload.imageUpload.apps.ImageuploadConfig',

    # PIP
    'minio_storage',
]

# REST_FRAMEWORK = {
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#     )
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fileUpload.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fileUpload.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

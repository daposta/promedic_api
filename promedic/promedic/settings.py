"""
Django settings for promedic project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '28i^qd5s^1uqf_-)a)f6wb4gwsg$_8gxr1iej2gk$09a-*m#79'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

ADMINS = [
    ('Oladapo Lawore', 'dapolawore@gmail.com')
]

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'oladapo'
EMAIL_HOST_PASSWORD = 'sunshine1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD = '??leviticus!!'
# EMAIL_HOST_USER = 'tryleviticuslabs@gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'PROMedic Admin<tryleviticuslabs@gmail.com>'

AUTHY_API_KEY ='lkw3UkxH2bWFa60ahEJTVebPHgYKwQHc'

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

MEDIA_URL = 'media/'

AUTH_USER_MODEL = 'core.Member'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['console'],
#             'level': 'ERROR',  # change debug level as appropiate
#             'propagate': False,
#         },
#     },
# }

REST_FRAMEWORK = {
   
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    #     'core.views.CustomJSONWebTokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
}

TWILIO_AUTH_TOKEN = '9844935a2bc2b2f61905f616c36cc814'
TWILIO_ACCOUNT_ID = 'AC0e35d1cac079a25d13ce99c5713d81d7'


JWT_AUTH = {
'JWT_RESPONSE_PAYLOAD_HANDLER': 'core.views.jwt_response_payload_handler',
'JWT_ALLOW_REFRESH': True,
'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),

}


CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000/',
    
# )
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'randompinfield',
    'core.apps.CoreConfig',
    'medic.apps.MedicConfig',
    'newsletters.apps.NewslettersConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]





ROOT_URLCONF = 'promedic.urls'

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

WSGI_APPLICATION = 'promedic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'promedicdb',  # os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'root',
        'PASSWORD': '0703',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

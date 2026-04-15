# Required packages:
#   pip install django python-dotenv psycopg2-binary stripe Pillow whitenoise gunicorn

import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql
pymysql.install_as_MySQLdb()

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-build-purposes')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
    '.now.sh',
    'beautyinblack.co.uk', 
    'www.beautyinblack.co.uk',
    'beautyinblack.wasmer.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://beautyinblack.co.uk',
    'https://www.beautyinblack.co.uk',
]

# ------------------------------------------------------------------------------
# PRODUCTION SECURITY HEADERS (only active when DEBUG=False)
# ------------------------------------------------------------------------------
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = False             # Vercel handles HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# ------------------------------------------------------------------------------
# DATABASE SECTION
# ------------------------------------------------------------------------------
DB_NAME = os.getenv('DB_NAME')

if not DB_NAME:
    if os.getenv('VERCEL'):
        raise ConnectionError("CRITICAL: DB_NAME environment variable is missing in Vercel Dashboard.")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}}
        }
    }  

# ------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = 'store.Customer'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ------------------------------------------------------------------------------
# INTERNATIONALISATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-gb'
TIME_ZONE     = 'Europe/London'
USE_I18N      = True
USE_TZ        = True

# ------------------------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------------------------
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
WHITENOISE_KEEP_FILES_ON_REMOTE = True

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------------------
# DEFAULT PK FIELD
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# STRIPE PAYMENTS
# ------------------------------------------------------------------------------
STRIPE_SECRET_KEY     = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY     = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# ------------------------------------------------------------------------------
# EMAIL (Gmail SMTP)
# ------------------------------------------------------------------------------
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = os.getenv('EMAIL_HOST_USER', 'noreply@beautyinblack.co.uk')

# ------------------------------------------------------------------------------
# SESSION
# ------------------------------------------------------------------------------
SESSION_COOKIE_AGE         = 1209600
SESSION_SAVE_EVERY_REQUEST = False
SESSION_ENGINE             = 'django.contrib.sessions.backends.signed_cookies'

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
#Black Is Beauty — ecommerce/settings.py
# REQUIRED packages - install before running:
#   pip install django python-dotenv psycopg2-binary stripe Pillow whitenoise
#updated: new static/template paths, media, email, Stripe.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── BASE ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG      = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# ─── APPS ────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',           # our main app
]


# ─── MIDDLEWARE ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serves static in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'


# ─── TEMPLATES ───────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look here FIRST, then in each app's own templates/ folder
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


# ─── DATABASE ────────────────────────────────────────────────────────────────
# SQLite is fine for development.
# Switch to PostgreSQL for production by setting DB_* env vars.
if os.getenv('DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     os.getenv('DB_NAME'),
            'USER':     os.getenv('DB_USER',     'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST':     os.getenv('DB_HOST',     'localhost'),
            'PORT':     os.getenv('DB_PORT',     '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   BASE_DIR / 'db.sqlite3',
        }
    }


# ─── AUTH ────────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'store.Customer'   # MUST match store/models.py

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'


# ─── INTERNATIONALISATION ────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-gb'
TIME_ZONE     = 'Europe/London'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True


# ─── STATIC FILES ────────────────────────────────────────────────────────────
# Source folders Django collects from:
#   - Each app's static/ subfolder  (APP_DIRS)
#   - The project-level static/ folder listed in STATICFILES_DIRS
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # where collectstatic writes files

STATICFILES_DIRS = [
    BASE_DIR / 'static',      # project-level static folder
                               # put your css/custom.css, images/logo-*.png etc. here
]

# Whitenoise compressed manifest storage (use in production)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ─── MEDIA FILES (uploaded images) ───────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─── STRIPE ──────────────────────────────────────────────────────────────────
STRIPE_SECRET_KEY    = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY    = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')


# ─── EMAIL ───────────────────────────────────────────────────────────────────
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER


# ─── SESSIONS ────────────────────────────────────────────────────────────────
SESSION_COOKIE_AGE     = 1_209_600   # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = False


# ─── MISC ────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
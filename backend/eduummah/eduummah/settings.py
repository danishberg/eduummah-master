from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# BASE_DIR configuration remains unchanged
BASE_DIR = Path(__file__).resolve().parent.parent

# Keep your secret key and debug setting as before
SECRET_KEY = 'django-insecure-nhz)7el26^)h@ix#9&e^@g((=r=-8tx+61bt=jmk$yb1)is%vl'
DEBUG = True
ALLOWED_HOSTS = []

# Installed apps, middleware, and other settings remain unchanged
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eduummah',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'verify_email.apps.VerifyEmailConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'eduummah.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent.parent / 'frontend' / 'build'],
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

WSGI_APPLICATION = 'eduummah.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent.parent / 'frontend' / 'build' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000']
CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000']
CSRF_COOKIE_SECURE = False # For production change to True | For dev change to False | Stage 1
SESSION_COOKIE_DOMAIN = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000'] # For dev | Stage 1 | None by default / for local testing
SESSION_COOKIE_SECURE = False # For dev | Stage 1 | True for HTTPS only
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # For dev | Stage 1 | Stores session data in the database
SESSION_COOKIE_HTTPONLY = True  # JavaScript should not access the session cookie
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # Set to True if you want browser-length sessions
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds

CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' if your frontend is on a different domain
SESSION_COOKIE_SAMESITE = 'Lax'  # or 'None' if your frontend is on a different domain
#SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax' # or Strict | Stage 2
#CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax' # or Strict | Stage 2
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000']

# CSRF and Session settings


CSRF_COOKIE_SECURE = False # For dev | Stage 1 |
SESSION_COOKIE_SECURE = False # For dev | Stage 1 | True for HTTPS only

VERIFY_EMAIL_LOGIN_URL_NAME = 'login'

LOGIN_URL = '/login/'

# Custom user model remains the same
AUTH_USER_MODEL = 'eduummah.CustomUser'

# Email settings now pull from .env file
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Print statements to verify the environment variables:
print("EMAIL_HOST_USER:", EMAIL_HOST_USER)
print("EMAIL_HOST_PASSWORD: [REDACTED]")  # Do not print the actual password.

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default ModelBackend
    'eduummah.backends.EmailAuthBackend',  # Your custom backend
]
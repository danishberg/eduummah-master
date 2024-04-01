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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
                 'DIRS': [os.path.join(BASE_DIR, 'frontend/build')],
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent.parent / 'frontend' / 'build' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000']
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:3000','http://127.0.0.1:8000']

VERIFY_EMAIL_LOGIN_URL_NAME = 'login'
LOGIN_URL = 'login'

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

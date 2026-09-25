"""
Django settings for portfolio_project project.
"""

from pathlib import Path

from decouple import config, Csv
import dj_database_url

try:
    import cloudinary
    import cloudinary.api
    import cloudinary.uploader
    import cloudinary_storage

    CLOUDINARY_AVAILABLE = True
except ImportError:  # pragma: no cover
    cloudinary = None
    cloudinary_storage = None
    CLOUDINARY_AVAILABLE = False


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-change-me-in-production'
)

DEBUG = config(
    'DEBUG',
    default=False,
    cast=bool
)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv()
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=Csv()
)


if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


# ============================================================
# CLOUDINARY
# ============================================================

CLOUDINARY_CLOUD_NAME = config(
    'CLOUDINARY_CLOUD_NAME',
    default=''
)

CLOUDINARY_API_KEY = config(
    'CLOUDINARY_API_KEY',
    default=''
)

CLOUDINARY_API_SECRET = config(
    'CLOUDINARY_API_SECRET',
    default=''
)

CLOUDINARY_ENABLED = (
    CLOUDINARY_AVAILABLE
    and not DEBUG
    and bool(CLOUDINARY_CLOUD_NAME)
    and bool(CLOUDINARY_API_KEY)
    and bool(CLOUDINARY_API_SECRET)
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'portfolio',
]


if CLOUDINARY_ENABLED:
    INSTALLED_APPS = [
        'cloudinary_storage',
        'cloudinary',
        *INSTALLED_APPS,
    ]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise serves collected static files in production.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = 'portfolio_project.urls'

WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

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


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


# ============================================================
# INTERNATIONALISATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# ============================================================
# MEDIA / CLOUDINARY STORAGE
# ============================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


if CLOUDINARY_ENABLED:

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )

    STORAGES = {
        'default': {
            'BACKEND':
                'cloudinary_storage.storage.MediaCloudinaryStorage',
        },

        'staticfiles': {
            'BACKEND':
                'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }

else:

    STORAGES = {
        'default': {
            'BACKEND':
                'django.core.files.storage.FileSystemStorage',
        },

        'staticfiles': {
            'BACKEND':
                'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }


# ============================================================
# MISC
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# EMAIL
# ============================================================

EMAIL_HOST = config(
    'EMAIL_HOST',
    default='smtp.gmail.com'
)

EMAIL_PORT = config(
    'EMAIL_PORT',
    default=587,
    cast=int
)

EMAIL_USE_TLS = config(
    'EMAIL_USE_TLS',
    default=True,
    cast=bool
)

EMAIL_USE_SSL = config(
    'EMAIL_USE_SSL',
    default=False,
    cast=bool
)

EMAIL_HOST_USER = config(
    'EMAIL_HOST_USER',
    default=''
)

EMAIL_HOST_PASSWORD = config(
    'EMAIL_HOST_PASSWORD',
    default=''
)

DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default=EMAIL_HOST_USER or 'josephineavomadoh@gmail.com'
)

EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default=(
        'django.core.mail.backends.smtp.EmailBackend'
        if EMAIL_HOST_USER
        else 'django.core.mail.backends.console.EmailBackend'
    )
)
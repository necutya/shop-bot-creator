import os

import redis
from dotenv import load_dotenv

# Use .env file for creating env variables
load_dotenv()

SITE_URL = os.getenv('SITE_URL')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"
MEDIA_DIRS = (os.path.join(BASE_DIR, "media"), "/media/")

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(int(os.getenv('DEBUG')))

TELEGRAM_BASE_URL = "https://api.telegram.org/bot%s/%s"

ROOT_URLCONF = "bots_settings.urls"

APPEND_SLASH = True
SAVE_MESSAGE = True
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "bots_management.apps.BotsManagementConfig",
    "administration.apps.AdministrationConfig",
    "subscribers.apps.SubscribersConfig",
    "bots_mailings.apps.BotsMailingsConfig",
    "moderators.apps.ModeratorsConfig",
    "products.apps.ProductsConfig",
    "orders.apps.OrdersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bots_settings.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('POSTGRES_DB'),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": os.getenv('POSTGRES_HOST'),
        "PORT": int(os.getenv('POSTGRES_PORT')),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation."
             "UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation."
             "MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation."
             "CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation."
             "NumericPasswordValidator", },
]

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

# Locale settings
LANGUAGE_CODE = "uk-UA"
# LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = "Europe/Kiev"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Email configurations
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Login redirect
LOGIN_URL = '/login/'

# Logging errors settings
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter_for_file': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'formatter_for_console': {
            'format': '\n {levelname} {asctime} {module} {process:d} {thread:d} {message} \n',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug_log.log',
            'formatter': 'formatter_for_file'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'formatter_for_console',
            'filters': ['require_debug_true'],
        },
        'console_django': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'formatter_for_console'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'console_on_not_debug': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'viber_api': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'telegram_api': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'bots_management': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'analytics': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': [
                'console_django',
                'mail_admins',
                'console_on_not_debug'
            ],
            'level': 'INFO',
        },
    }
}
# add your email for getting mails with critical errors


ADMINS = [(env.get('ADMIN_NAME'), env.get('ADMIN_EMAIL'))]
"""

# DATE_SETTINGS
DATE_FORMAT = "%d.%m.%Y"

# celery settings looks like redis://localhost:6379
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

# Use nose to run all tests
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
# NOSE_ARGS = [
#     '--with-coverage',
#     '--cover-package=moderators',
#     '--cover-html'
# ]

redis_instance = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
)

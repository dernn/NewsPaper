"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

from dotenv import dotenv_values  # use python-dotenv

config = dotenv_values()  # include all values from .env like dict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'modeltranslation',  # обязательно перед админом [D17.4]
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
    'accounts',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'django_filters',
    # приложение для проверки аутентификации
    'protect',
    # первая реализация регистрации;
    # редактирование профиля
    'sign',
    # приложение сигналов и рассылки:
    # подключение кастомного конфига (apps.MailingConfig)
    'mailing.apps.MailingConfig',
    # for D9.5: weekly mailing
    'django_apscheduler',
    'rest_framework',  # [D18.6]
    'drf_spectacular',

    # приложения allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... регистрация посредством провайдера:
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # enables language selection based on data from the request
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # настройки middleware для allauth
    "allauth.account.middleware.AccountMiddleware",
    'news.middlewares.TimezoneMiddleware',  # custom timezone middleware
]

ROOT_URLCONF = 'NewsPaper.urls'

# for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

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
                'news.context_processors.tz_ctime',  # добавляем tz-контекст для всех вьюшек
            ],
        },
    },
]

# URL-адрес аутентификации
# LoginRequiredMixin перенаправит пользователя на эту страницу
LOGIN_URL = '/accounts/login/'
# редирект после успешного входа на сайт
LOGIN_REDIRECT_URL = '/'

# используется в случае, если данный проект управляет несколькими сайтами
SITE_ID = 1

# Бэкенды аутентификации [для allauth]
AUTHENTICATION_BACKENDS = [
    # встроенный бэкенд Django, реализующий аутентификацию по username
    'django.contrib.auth.backends.ModelBackend',
    # бэкенд аутентификации, предоставленный пакетом allauth:
    # по email или сервис-провайдеру
    'allauth.account.auth_backends.AuthenticationBackend',
]

# настройки allauth для входа/регистрации по email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# username не требуется
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# подтверждение почты отключено
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# замена стандартной формы регистрации кастомной
ACCOUNT_FORMS = {'signup': 'sign.forms.BasicSignupForm'}

# активирует аккаунт при переходе по ссылке [D9.3]
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# количество дней "жизни" ссылки на подтверждение регистрации (default: 3)
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
LANGUAGES = [
    ("ru", "Russian"),
    ("en", "English"),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# for django.core.mail
EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты
EMAIL_PORT = 465  # порт smtp сервера
# имя пользователя [до @domain]
EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = config['DEFAULT_FROM_EMAIL']
SITE_URL = 'http://127.0.0.1:8000'

# for D9.5: weekly mailing
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format
# for format string syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# for D10.3: Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# triggered repeatedly
# CELERY_ENABLE_UTC = False  # because of this

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# for D11.3: Filesystem caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # Указываем, куда будем сохранять кэшируемые файлы
        # Не забываем создать папку cache_files внутри папки с manage.py
        'LOCATION': BASE_DIR / 'cache_files',
        'TIMEOUT': 60,  # 60 sec; default value 300
    }
}

# for D16.4: Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'simple_warning': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        },
        'simple_error': {
            'format': '%(asctime)s %(levelname)s %(message)s %(exc_info)s'
        },
        'general': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'errors': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'security': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'mail_admins': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        },
    },
    # p.extra RequireDebug
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # p.1 Send all messages to console
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_error',
        },
        # p.2 Send INFO messages to general.log
        'file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'general',
            'filename': 'logs/general.log'
        },
        # p.3 Send ERROR messages to errors.log
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'errors'
        },
        # p.4 Send INFO messages from django.security to security.log
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'security'
        },
        # p.5 ERROR messages are sent to admin emails
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail_admins'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'file_general'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins', ],
            'level': 'ERROR',
            # все сообщение дочерних журналов логирования также попадают в родительский ['django']
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_errors', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file_errors', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file_security', ],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

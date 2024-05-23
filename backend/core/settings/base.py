
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# work with env variables
from decouple import config

from django.utils.translation import gettext_lazy as _


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
print(f'{PROJECT_DIR=}')
print(f'{BASE_DIR=}')

# DEBUG = False
DEBUG = config('DEBUG', default=False, cast=bool)
print(f'base config: loaded DEBUG={DEBUG}')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", "not-loaded-secret-key-ryu_zr&i&2ne6kXt9uib5oy8rca6ygb5tv!5hb#po-%%9hn2_43k")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    'wagtail.contrib.settings',  # site settings https://docs.wagtail.org/en/v3.0.1/reference/contrib/settings.html
    "wagtail_modeladmin",  # >5.1  https://wagtailmenus.readthedocs.io/en/stable/installation.html
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # src
    "menus.apps.MenusConfig",
    "project.apps.ProjectConfig",
    "tvweek.apps.TvweekConfig",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'wagtail.contrib.settings.context_processors.settings',  # added
                'home.context_processors.contact_form',  # added for contact form
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    # Database PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': config('SQL_ENGINE', default=''),
            'NAME': config('SQL_DATABASE', default=''),
            'USER': config("SQL_USER", default=''),
            'PASSWORD': config("SQL_PASSWORD", default=''),
            'HOST': config("SQL_HOST", default=''),
            'PORT': config("SQL_PORT", default=''),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "uk"

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('uk', _('Ukrainian')),
    ('en', _('English')),
]

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Sets default for primary key IDs
# See https://docs.djangoproject.com/en/4.1/ref/models/fields/#bigautofield
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}


# Wagtail settings
CSRF_TRUSTED_ORIGINS = [
    'https://*.svitlo.tv',
    'http://10.1.100.173',
]
WAGTAIL_SITE_NAME = config('WAGTAIL_SITE_NAME', default="core")

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = config('WAGTAILADMIN_BASE_URL', default='https://svitlo.tv/')

WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]

# Wagtail settings options
# https://docs.wagtail.org/en/stable/reference/settings.html
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = config('WAGTAILADMIN_NOTIFICATION_FROM_EMAIL', default='')
WAGTAILUSERS_PASSWORD_REQUIRED = config('WAGTAILUSERS_PASSWORD_REQUIRED', default=True, cast=bool)
WAGTAILADMIN_NOTIFICATION_USE_HTML = config('WAGTAILADMIN_NOTIFICATION_USE_HTML', default=True, cast=bool)
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = config('WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS',
                                                      default=False,
                                                      cast=bool
                                                      )

# EMAIL settings
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='a-email:')

# ADMINS = [('asite admin1', 'a.voznyuk@film.ua'), ('asite admin2', 'andreyv@ukr.net')]
ADMINS = [('asite admin2', 'andreyv@ukr.net')]

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = f"{DEFAULT_FROM_EMAIL}"

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# frontend login settings
# https://learnwagtail.com/tutorials/adding-user-authentication-registration-and-login-your-wagtail-website/
LOGIN_URL = config('LOGIN_URL', default='/login_/')
ACCOUNT_LOGOUT_REDIRECT_URL = config('ACCOUNT_LOGOUT_REDIRECT_URL', default='/login_/')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/_/')

ACCOUNT_AUTHENTICATION_METHOD = config('ACCOUNT_AUTHENTICATION_METHOD', default="username_email")
ACCOUNT_CONFIRM_EMAIL_ON_GET = config('ACCOUNT_CONFIRM_EMAIL_ON_GET', default=False, cast=bool)
ACCOUNT_EMAIL_REQUIRED = config('ACCOUNT_EMAIL_REQUIRED', default=True, cast=bool)
ACCOUNT_EMAIL_VERIFICATION = config('ACCOUNT_EMAIL_VERIFICATION', default="optional")
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = config('ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION', default=True, cast=bool)
ACCOUNT_LOGOUT_ON_GET = config('ACCOUNT_LOGOUT_ON_GET', default=True, cast=bool)
ACCOUNT_LOGIN_ON_PASSWORD_RESET = config('ACCOUNT_LOGIN_ON_PASSWORD_RESET', default=True, cast=bool)
ACCOUNT_PRESERVE_USERNAME_CASING = config('ACCOUNT_PRESERVE_USERNAME_CASING', default=False, cast=bool)
ACCOUNT_SESSION_REMEMBER = config('ACCOUNT_SESSION_REMEMBER', default=True, cast=bool)
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = config('ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE', default=False, cast=bool)
ACCOUNT_USERNAME_BLACKLIST = config('ACCOUNT_USERNAME_BLACKLIST', default=["admin1", "root1"])
ACCOUNT_USERNAME_MIN_LENGTH = config('ACCOUNT_USERNAME_MIN_LENGTH', default=4, cast=int)


LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name} {levelname} {module} {message}',
            'style':  '{',
        },
        'simple':  {
            'format': '{asctime} {levelname} {message}',
            'style':  '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log

    #    DEBUG (10) detailed
    #    INFO (20) informational, all ok but let me know that
    #    WARNING (30) something wrong, but application will continue
    #    ERROR (40) application can`t do someting
    #    CRITICAL (50) application will crash

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/' + 'warning.log',
            'formatter': 'verbose'
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
        'project': {
            'handlers':  ['file'],  # notice how file variable is called in handler which has been defined above
            'level':     'INFO',  # CRITICAL ERROR WARNING INFO DEBUG
            'propagate': True,
            'formatter': 'verbose'
        },
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['console', 'file'], #notice how file variable is called in handler which has been defined above
            'level': 'DEBUG',
            'propagate': True,
            'formatter': 'verbose'
        },
    },
}


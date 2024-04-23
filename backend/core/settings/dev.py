from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
print(f'DEBUG.dev={DEBUG} ')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+$d#&btb)wb$71i1#0eellbko%#m1+bfm^ek+%(h^9hqo8od9d"

ALLOWED_HOSTS = [
    "selected12309.svitlo.tv",
    "svitlo.tv",
    "10.1.100.173",
    "127.0.0.1",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = [
    'https://*.svitlo.tv',
    'http://10.1.100.173',
]
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    "selected12309.svitlo.tv",
    "svitlo.tv",
    "10.1.100.173",
]
CSRF_TRUSTED_ORIGINS = [
    'https://selected12309.svitlo.tv/',
    'http://10.1.100.173:8111/',
]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


try:
    from .local import *
except ImportError:
    pass

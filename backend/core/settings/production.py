from .base import *

import logging


logger = logging.getLogger(__name__)
logger.info("Loaded DEVELOPER settings.")


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

from .base import *

import logging
logger = logging.getLogger(__name__)
logger.info("Loaded PRODUCTION settings.")

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

print(f'DEBUG.production={DEBUG} ')

ALLOWED_HOSTS = [
    "selected12309.svitlo.tv",
    "svitlo.tv",
    "10.1.100.173",
]
CSRF_TRUSTED_ORIGINS = [
    'https://*.svitlo.tv',
    'http://10.1.100.173',
]
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


try:
    from .local import *
except ImportError:
    pass

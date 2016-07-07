from base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local import *  # noqa
except ImportError:
    pass

from dj_start.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']
INSTALLED_APPS += (
    'debug_toolbar',
)
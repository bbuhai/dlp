from dj_start.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#ALLOWED_HOSTS = ['*']
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

DATABASES = {
    "default": {
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': ':memory:'
    }
}
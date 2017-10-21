"""
Settings in development environment.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DEV_ONLY_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + DEV_ONLY_APPS

DEV_ONLY_MIDDLEWARE = []

MIDDLEWARE = PREREQ_MIDDLEWARE + PROJECT_MIDDLEWARE + DEV_ONLY_MIDDLEWARE

MEDIA_ROOT = '~/Pictures/shawnslab/'

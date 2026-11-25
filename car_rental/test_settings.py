"""Isolated regression settings; no production database or uploaded documents."""
from .settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
SECRET_KEY = 'synthetic-test-only-key'
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
OCR_STORE_UPLOADS = False

from .settings import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}

SECRET_KEY='^68jw2hq_=v44xhz7=pw-%odaq+w=7)-xh8qobalp^ib%!l_x^'

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'hello@librecipes.com'
EMAIL_USE_TLS = False
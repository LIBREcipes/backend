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
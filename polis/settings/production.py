from polis.settings.common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRE_HOST', '127.0.0.1'),
        'PORT': int(os.environ.get('POSTGRE_PORT', '5432')),
        'USER': os.environ.get('POSTGRE_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRE_PASSWORD', 'root'),
        'NAME': os.environ.get('POSTGRE_DATABASE', 'polis'),
    }
}

ALLOWED_HOSTS = [
    '0.0.0.0.',
    '127.0.0.1',
    'localhost',
]

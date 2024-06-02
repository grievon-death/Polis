from settings.common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'host': os.environ.get('POSTGRE_HOST', '127.0.0.1'),
        'port': int(os.environ.get('POSTGRE_PORT', '5432')),
        'user': os.environ.get('POSTGRE_USER', 'postgres'),
        'password': os.environ.get('POSTGRE_PASSWORD', 'root'),
        'db': os.environ.get('POSTGRE_DATABASE', 'polis'),
    }
}

ALLOWED_HOSTS = [
    '0.0.0.0.',
    '127.0.0.1',
    'localhost',
]

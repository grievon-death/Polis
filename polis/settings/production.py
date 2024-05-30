from settings.common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'host': os.environ.get('POSTGRE_HOST'),
        'port': int(os.environ.get('POSTGRE_PORT', '3306')),
        'user': os.environ.get('POSTGRE_USER'),
        'password': os.environ.get('POSTGRE_PASSWORD'),
    }
}

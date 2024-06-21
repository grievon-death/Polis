dev_migrate:
	python3 manage.py makemigrations --settings=polis.settings.common
	python3 manage.py migrate --settings=polis.settings.common

development:
	python3 manage.py migrate --settings=polis.settings.common
	python3 manage.py runserver 0.0.0.0:8008 --settings=polis.settings.common

production:
	python3 manage.py migrate --settings=polis.settings.production
	gunicorn -w 3  -b :8008 --env DJANGO_SETTINGS_MODULE=polis.settings.production polis.wsgi:application

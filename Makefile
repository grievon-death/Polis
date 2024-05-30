dev_migrate:
	python3 manage.py makemigrations --settings=polis.settings.common
	python3 manage.py migrate --settings=polis.settings.common

migrate:
	python3 manage.py migrate --settings=polis.settings.production

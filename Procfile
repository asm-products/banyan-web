web: gunicorn banyan.wsgi --log-file -
worker: celery -A banyan worker -l info -B


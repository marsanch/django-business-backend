web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4
celery: celery -A config worker -l info
beat: celery -A config beat -l info


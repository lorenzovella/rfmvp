release: python manage.py migrate --run-syncdb
web: daphne clientflow.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2

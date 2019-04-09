web: daphne -b 0.0.0.0 -p $PORT koda.asgi:application -v2 && gunicorn koda.wsgi --log-file -
worker: python manage.py runworker -v2

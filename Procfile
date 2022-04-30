web: gunicorn bookstore.wsgi
release: python manage.py migrate
worker: celery -A bookstore worker -l INFO -P solo
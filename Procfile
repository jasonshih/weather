web: python manage.py collectstatic --noinput --settings=weather.settings.prod; gunicorn_django --workers=1 --bind=0.0.0.0:$PORT weather/settings/prod.py

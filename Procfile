web: sh -c "python manage.py migrate --noinput > /tmp/migrate.log 2>&1 & (sleep 10 && python manage.py seed_data > /tmp/seed.log 2>&1) & gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --timeout 120 --access-logfile -"
release: python manage.py migrate --noinput

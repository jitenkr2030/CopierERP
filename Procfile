web: sh -c "python manage.py migrate --noinput && python manage.py seed_data --noinput || true && python manage.py runserver 0.0.0.0:${PORT:-8000}"

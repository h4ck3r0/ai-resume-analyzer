web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class sync --max-requests 10 --max-requests-jitter 2 --timeout 120 --access-logfile - --error-logfile - wsgi:app

#!/bin/sh

# Inicia Celery Worker
celery -A app_monitor worker --loglevel=info &

# Inicia Celery Beat
celery -A app_monitor beat --loglevel=info &

# Mantiene el contenedor activo para evitar que se detenga
tail -f /dev/null

#!/bin/bash

# Waiting for the database to be ready
# echo "Waiting for the database to be ready"
# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 0.1
# done

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Update All Permissions for all apps
echo "Update All Permissions for all apps"
python manage.py update_all_permissions

# Add Default Group
echo "Add Default Group"
python manage.py create_default_groups

# Add Default Menu
echo "Add Default Menu"
python manage.py create_default_menus

# Start server
echo "Starting server"
if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "Using Django development server"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Using Gunicorn"
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi
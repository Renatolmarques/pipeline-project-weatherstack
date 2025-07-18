#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Install local python packages
if [ -f "/app/docker/requirements-local.txt" ]; then
  echo "Installing local python packages..."
  pip install -r /app/docker/requirements-local.txt
fi

# Initialize/Upgrade Superset's metadata database
echo "Upgrading Superset metadata database..."
superset db upgrade

# Start the Superset web server in the foreground
echo "Starting Superset web server on port 8088"
gunicorn \
  --bind "0.0.0.0:8088" \
  --access-logfile "-" \
  --error-logfile "-" \
  --workers 1 \
  --worker-class gthread \
  "superset.app:create_app()"
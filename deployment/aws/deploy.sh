#!/bin/bash
# Deployment script for updates

PROJECT_DIR="/var/www/shivank_kirana"

echo "Starting deployment..."
cd $PROJECT_DIR || { echo "Project directory not found!"; exit 1; }

echo "Pulling latest code from repository..."
git pull origin main

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/Updating dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting Gunicorn service..."
sudo systemctl restart gunicorn

echo "Restarting Nginx service..."
sudo systemctl restart nginx

echo "Deployment completed successfully!"

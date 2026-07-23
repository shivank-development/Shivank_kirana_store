#!/bin/bash
# EC2 Setup Script for Ubuntu 22.04/24.04
# Run this script on a fresh EC2 instance to prepare the environment

set -e

echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

echo "Installing essential packages..."
sudo apt-get install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git redis-server certbot python3-certbot-nginx

echo "Setting up project directory..."
sudo mkdir -p /var/www/shivank_kirana
sudo chown -R $USER:www-data /var/www/shivank_kirana
sudo chmod -R 775 /var/www/shivank_kirana

echo "Creating log directories for Gunicorn..."
sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:www-data /var/log/gunicorn

echo "EC2 Setup complete. Please clone the repository into /var/www/shivank_kirana."

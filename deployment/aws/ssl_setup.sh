#!/bin/bash
# SSL Setup script using Certbot
# Make sure your DNS A record points to your EC2 instance IP before running this.

DOMAIN="your_domain.com" # Replace with your actual domain

echo "Setting up SSL for $DOMAIN..."

# Ensure certbot is installed
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain and install SSL certificate via Nginx plugin
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN

echo "SSL setup complete! Certbot will automatically renew your certificates."
echo "You can test auto-renewal with: sudo certbot renew --dry-run"

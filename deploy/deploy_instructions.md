# AWS EC2 Deployment Guide (Ubuntu 22.04 LTS)

Follow these steps to deploy Shivank Kirana Store on your AWS EC2 instance.

## 1. Initial Server Setup

SSH into your EC2 instance and update the system:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

## 2. Clone Repository & Setup Environment

```bash
# Clone the repo (replace with your repo link)
git clone <your_github_repo_url> Shivank-Kirana-Store
cd Shivank-Kirana-Store

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Prepare Django for Production

In `config/settings/base.py` (or `.env`):
- Set `DEBUG = False`
- Set `ALLOWED_HOSTS = ['your_domain.com', 'your_server_ip']`

Run migrations and collect static files:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

## 4. Setup Gunicorn

Copy the provided gunicorn service file to systemd:
```bash
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

*Check gunicorn status to ensure it's running:*
```bash
sudo systemctl status gunicorn
```

## 5. Setup Nginx

Copy the provided nginx config file:
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/shivank_store
sudo ln -s /etc/nginx/sites-available/shivank_store /etc/nginx/sites-enabled/
```

Test Nginx config and restart:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Setup SSL (HTTPS) with Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

Your site should now be live and secure! 🚀

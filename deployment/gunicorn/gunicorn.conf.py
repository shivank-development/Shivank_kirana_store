import multiprocessing

# Gunicorn configuration for production
bind = "unix:/var/www/shivank_kirana/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120

# Logging
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"

# Module to run
wsgi_app = "config.wsgi:application"

import os

apps = ['cart', 'wishlist', 'orders', 'delivery', 'payments', 'notifications', 'analytics', 'import_export', 'chatbot', 'support', 'home', 'checkout', 'search', 'admin_panel', 'categories', 'brands']

base = r'c:\Users\offic\Desktop\Gemini\apps'

for app in apps:
    app_dir = os.path.join(base, app)
    os.makedirs(app_dir, exist_ok=True)
    
    init_file = os.path.join(app_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write(f'# {app} app\n')
    
    apps_file = os.path.join(app_dir, 'apps.py')
    if not os.path.exists(apps_file):
        class_name = ''.join(word.capitalize() for word in app.replace('_', ' ').split()) + 'Config'
        display_name = app.replace('_', ' ').title()
        with open(apps_file, 'w') as f:
            f.write(f'from django.apps import AppConfig\n\nclass {class_name}(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "apps.{app}"\n    verbose_name = "{display_name}"\n')
    
    urls_file = os.path.join(app_dir, 'urls.py')
    if not os.path.exists(urls_file):
        with open(urls_file, 'w') as f:
            f.write(f'from django.urls import path\n\nurlpatterns = []\n')
    
    views_file = os.path.join(app_dir, 'views.py')
    if not os.path.exists(views_file):
        with open(views_file, 'w') as f:
            f.write(f'# {app} views\n')
    
    admin_file = os.path.join(app_dir, 'admin.py')
    if not os.path.exists(admin_file):
        with open(admin_file, 'w') as f:
            f.write(f'from django.contrib import admin\n')

print('All app stubs created!')

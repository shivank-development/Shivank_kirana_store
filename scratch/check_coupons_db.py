import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection

print("--- RAW COUPONS TABLE CONTENT ---")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(coupons)")
    columns = [row[1] for row in cursor.fetchall()]
    print("Columns:", columns)
    
    cursor.execute("SELECT * FROM coupons")
    rows = cursor.fetchall()
    print(f"Total raw rows: {len(rows)}")
    for r in rows:
        print(r)

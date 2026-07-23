import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.products.models.category import Category

CATEGORIES = [
    "Grains & Pulses",
    "Atta/Rice & Flour",
    "Spices & Masala",
    "Tea/Coffee & Beverages",
    "Edible Oil & Ghee",
    "Snacks & Branded Foods",
    "Personal Care",
    "Home Care",
    "Baby Care",
    "Dairy & Bakery",
    "Frozen Foods",
    "Pooja & Essentials"
]

def seed_categories():
    print("🌿 Seeding Categories for Shivank Kirana Store...")
    for idx, name in enumerate(CATEGORIES):
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={
                'sort_order': idx + 1
            }
        )
        if created:
            print(f"✅ Created category: {name}")
        else:
            print(f"ℹ️ Category already exists: {name}")
            
    print(f"🎉 Seeding complete! Total categories in DB: {Category.objects.count()}")

if __name__ == '__main__':
    seed_categories()

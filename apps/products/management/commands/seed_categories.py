from django.core.management.base import BaseCommand
from apps.products.models.category import Category

class Command(BaseCommand):
    help = 'Seeds the database with 12 initial categories'

    def handle(self, *args, **kwargs):
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

        self.stdout.write(self.style.NOTICE("Seeding Categories for Shivank Kirana Store..."))
        
        for idx, name in enumerate(CATEGORIES):
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'sort_order': idx + 1
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {name}"))
                
        self.stdout.write(self.style.SUCCESS(f"Seeding complete! Total categories in DB: {Category.objects.count()}"))

from django.core.management.base import BaseCommand
from apps.products.models.brand import Brand

class Command(BaseCommand):
    help = 'Seeds the database with 20 initial brands'

    def handle(self, *args, **kwargs):
        BRANDS = [
            "Amul", "Aashirvaad", "Britannia", "Cadbury", "Chupa Chups", 
            "Colgate", "Dabur", "Fortune", "Haldiram's", "KitKat", 
            "Lay's", "Lifebuoy", "Maggi", "M&M's", "Nestlé", 
            "Oreo", "Parle", "Surf Excel", "Tata", "Tic Tac"
        ]

        self.stdout.write(self.style.NOTICE("Seeding Brands for Shivank Kirana Store..."))
        
        for idx, name in enumerate(BRANDS):
            brand, created = Brand.objects.get_or_create(
                name=name,
                defaults={
                    'sort_order': idx + 1
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created brand: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Brand already exists: {name}"))
                
        self.stdout.write(self.style.SUCCESS(f"Seeding complete! Total brands in DB: {Brand.objects.count()}"))

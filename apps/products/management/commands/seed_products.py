from django.core.management.base import BaseCommand
from apps.products.models.product import Product
from apps.products.models.category import Category
from apps.products.models.brand import Brand
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample products'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding Products for Shivank Kirana Store..."))

        # Fetch some categories and brands
        try:
            cat_snacks = Category.objects.filter(name__icontains="Snacks").first()
            cat_dairy = Category.objects.filter(name__icontains="Dairy").first()
            cat_beverages = Category.objects.filter(name__icontains="Beverages").first()
            cat_spices = Category.objects.filter(name__icontains="Spices").first()
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Please run 'python manage.py seed_categories' first."))
            return

        brands = {b.name: b for b in Brand.objects.all()}

        # Sample Products Data
        sample_products = [
            {
                "name": "Lay's India's Magic Masala Potato Chips",
                "category": cat_snacks,
                "brand": brands.get("Lay's"),
                "price": 20.0,
                "discount_price": 18.0,
                "weight": "50g",
                "stock": 100,
                "is_featured": True
            },
            {
                "name": "Amul Taaza Homogenised Toned Milk",
                "category": cat_dairy,
                "brand": brands.get("Amul"),
                "price": 72.0,
                "discount_price": 70.0,
                "weight": "1L",
                "stock": 50,
                "is_featured": True
            },
            {
                "name": "Tata Tea Premium",
                "category": cat_beverages,
                "brand": brands.get("Tata"),
                "price": 150.0,
                "discount_price": 135.0,
                "weight": "250g",
                "stock": 200,
                "is_featured": False
            },
            {
                "name": "Maggi 2-Minute Instant Noodles",
                "category": cat_snacks,
                "brand": brands.get("Maggi"),
                "price": 14.0,
                "discount_price": 14.0,
                "weight": "70g",
                "stock": 300,
                "is_featured": True
            },
            {
                "name": "Aashirvaad Shudh Chakki Atta",
                "category": Category.objects.filter(name__icontains="Atta").first(),
                "brand": brands.get("Aashirvaad"),
                "price": 250.0,
                "discount_price": 230.0,
                "weight": "5kg",
                "stock": 40,
                "is_featured": True
            },
            {
                "name": "Cadbury Dairy Milk Silk Chocolate",
                "category": cat_snacks,
                "brand": brands.get("Cadbury"),
                "price": 80.0,
                "discount_price": 75.0,
                "weight": "60g",
                "stock": 150,
                "is_featured": True
            },
            {
                "name": "Fortune Sunlite Refined Sunflower Oil",
                "category": Category.objects.filter(name__icontains="Oil").first(),
                "brand": brands.get("Fortune"),
                "price": 140.0,
                "discount_price": 125.0,
                "weight": "1L",
                "stock": 80,
                "is_featured": False
            },
            {
                "name": "Surf Excel Easy Wash Detergent Powder",
                "category": Category.objects.filter(name__icontains="Home").first(),
                "brand": brands.get("Surf Excel"),
                "price": 130.0,
                "discount_price": 118.0,
                "weight": "1kg",
                "stock": 90,
                "is_featured": False
            },
        ]

        for p_data in sample_products:
            if not p_data['category']:
                continue
            
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'category': p_data['category'],
                    'brand': p_data['brand'],
                    'price': p_data['price'],
                    'discount_price': p_data['discount_price'],
                    'weight': p_data['weight'],
                    'stock': p_data['stock'],
                    'is_featured': p_data['is_featured'],
                    'rating_avg': round(random.uniform(3.8, 5.0), 1),
                    'rating_count': random.randint(10, 500)
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product already exists: {product.name}"))

        self.stdout.write(self.style.SUCCESS(f"Seeding complete! Total products in DB: {Product.objects.count()}"))

"""
Seed script — Populates Shivank Kirana Store with initial data.
Run: python scripts/seed_data.py
"""
import os
import sys
import django
import shutil
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.products.models import Category, Brand, Product
from apps.orders.models import StoreSettings


def create_categories():
    """Create 12 product categories."""
    cats = [
        {'name': 'Grains & Pulses',        'slug': 'grains-pulses',           'sort_order': 1,
         'description': 'Atta, Dal, Rice, Pulses'},
        {'name': 'Atta, Rice & Flour',     'slug': 'atta-rice-flour',         'sort_order': 2,
         'description': 'Chakki Atta, Basmati Rice'},
        {'name': 'Snacks & Branded Foods', 'slug': 'snacks-branded-foods',    'sort_order': 3,
         'description': "Lay's, Haldiram's, Kurkure, Parle"},
        {'name': 'Dairy & Bakery',         'slug': 'dairy-bakery',            'sort_order': 4,
         'description': 'Amul, Britannia, Milk, Curd'},
        {'name': 'Spices & Masala',        'slug': 'spices-masala',           'sort_order': 5,
         'description': 'MDH, Everest, Tata Sampann'},
        {'name': 'Tea, Coffee & Beverages','slug': 'tea-coffee-beverages',    'sort_order': 6,
         'description': 'Tata Tea, Nescafé, Red Bull'},
        {'name': 'Edible Oil & Ghee',      'slug': 'edible-oil-ghee',         'sort_order': 7,
         'description': 'Fortune, Dhara, Amul Ghee'},
        {'name': 'Personal Care',          'slug': 'personal-care',           'sort_order': 8,
         'description': 'Colgate, Dove, Dettol, HUL'},
        {'name': 'Home Care',              'slug': 'home-care',               'sort_order': 9,
         'description': 'Surf Excel, Lizol, Harpic'},
        {'name': 'Baby Care',              'slug': 'baby-care',               'sort_order': 10,
         'description': "Johnson's, Pampers, Cerelac"},
        {'name': 'Frozen Foods',           'slug': 'frozen-foods',            'sort_order': 11,
         'description': "McCain, Haldiram's Frozen"},
        {'name': 'Pooja Essentials',       'slug': 'pooja-essentials',        'sort_order': 12,
         'description': 'Agarbatti, Diyas, Camphor'},
    ]
    
    created = 0
    for cat_data in cats:
        obj, new = Category.objects.get_or_create(
            slug=cat_data['slug'], defaults={**cat_data, 'is_active': True}
        )
        if new:
            created += 1
    print(f'[OK] Categories: {created} created, {len(cats)-created} already existed')
    return Category.objects.all()


def create_brands():
    """Create major FMCG brands."""
    brands = [
        {'name': "Lay's",         'slug': 'lays',        'sort_order': 1},
        {'name': 'Haldiram\'s',   'slug': 'haldirams',   'sort_order': 2},
        {'name': 'KitKat',        'slug': 'kitkat',      'sort_order': 3},
        {'name': 'Cadbury',       'slug': 'cadbury',     'sort_order': 4},
        {'name': 'Amul',          'slug': 'amul',        'sort_order': 5},
        {'name': 'Britannia',     'slug': 'britannia',   'sort_order': 6},
        {'name': 'Tata',          'slug': 'tata',        'sort_order': 7},
        {'name': 'Nestlé',        'slug': 'nestle',      'sort_order': 8},
        {'name': 'Parle',         'slug': 'parle',       'sort_order': 9},
        {'name': 'ITC',           'slug': 'itc',         'sort_order': 10},
        {'name': 'Maggi',         'slug': 'maggi',       'sort_order': 11},
        {'name': 'Bingo',         'slug': 'bingo',       'sort_order': 12},
        {'name': 'Kurkure',       'slug': 'kurkure',     'sort_order': 13},
        {'name': 'Oreo',          'slug': 'oreo',        'sort_order': 14},
        {'name': 'MDH',           'slug': 'mdh',         'sort_order': 15},
        {'name': 'Everest',       'slug': 'everest',     'sort_order': 16},
        {'name': 'Dove',          'slug': 'dove',        'sort_order': 17},
        {'name': 'Colgate',       'slug': 'colgate',     'sort_order': 18},
        {'name': 'Dettol',        'slug': 'dettol',      'sort_order': 19},
        {'name': "Lay's (Big)",   'slug': 'lays-big',    'sort_order': 20},
        {'name': 'Fortune',       'slug': 'fortune',     'sort_order': 21},
    ]
    
    created = 0
    for b in brands:
        obj, new = Brand.objects.get_or_create(
            slug=b['slug'], defaults={**b, 'is_active': True}
        )
        if new:
            created += 1
    print(f'[OK] Brands: {created} created, {len(brands)-created} already existed')
    return Brand.objects.all()


def create_sample_products():
    """Create sample products from the brand list."""
    snacks = Category.objects.filter(slug='snacks-branded-foods').first()
    dairy  = Category.objects.filter(slug='dairy-bakery').first()
    spices = Category.objects.filter(slug='spices-masala').first()
    grains = Category.objects.filter(slug='grains-pulses').first()
    
    lays      = Brand.objects.filter(slug='lays').first()
    haldirams = Brand.objects.filter(slug='haldirams').first()
    kitkat    = Brand.objects.filter(slug='kitkat').first()
    amul      = Brand.objects.filter(slug='amul').first()
    britannia = Brand.objects.filter(slug='britannia').first()
    maggi     = Brand.objects.filter(slug='maggi').first()
    oreo      = Brand.objects.filter(slug='oreo').first()
    cadbury   = Brand.objects.filter(slug='cadbury').first()
    kurkure   = Brand.objects.filter(slug='kurkure').first()
    
    products = [
        # Lay's
        {'name': "Lay's Classic Salted Chips", 'brand': lays, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '26g', 'stock': 100,
         'is_featured': True, 'rating_avg': 4.3, 'rating_count': 128, 'bought_count': 325,
         'delivery_eta': 'Tomorrow'},
        {'name': "Lay's Magic Masala", 'brand': lays, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '26g', 'stock': 80,
         'is_featured': True, 'rating_avg': 4.5, 'rating_count': 256, 'bought_count': 480},
        {'name': "Lay's American Style Cream & Onion", 'brand': lays, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '26g', 'stock': 60,
         'is_featured': True, 'rating_avg': 4.2, 'rating_count': 95},
        {'name': "Lay's West Indies Hot 'n' Sweet Chilli", 'brand': lays, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '26g', 'stock': 55},
        {'name': "Lay's India's Magic Masala Family Pack", 'brand': lays, 'category': snacks,
         'price': 60, 'discount_price': 55, 'weight': '108g', 'stock': 40, 'is_featured': True},
        
        # KitKat
        {'name': 'KitKat Chocolate 4 Finger', 'brand': kitkat, 'category': snacks,
         'price': 35, 'discount_price': 32, 'weight': '41.5g', 'stock': 200,
         'is_featured': True, 'rating_avg': 4.7, 'rating_count': 342, 'bought_count': 600},
        {'name': 'KitKat Mini Moments', 'brand': kitkat, 'category': snacks,
         'price': 90, 'discount_price': 82, 'weight': '200g', 'stock': 80, 'is_featured': True},
        {'name': 'KitKat Senses Hazelnut', 'brand': kitkat, 'category': snacks,
         'price': 150, 'discount_price': 135, 'weight': '150g', 'stock': 50},
        
        # Haldiram's
        {'name': "Haldiram's Aloo Bhujia", 'brand': haldirams, 'category': snacks,
         'price': 40, 'discount_price': 36, 'weight': '200g', 'stock': 150,
         'is_featured': True, 'rating_avg': 4.4, 'rating_count': 215, 'bought_count': 400},
        {'name': "Haldiram's Bhujia Sev", 'brand': haldirams, 'category': snacks,
         'price': 30, 'discount_price': 27, 'weight': '150g', 'stock': 120},
        {'name': "Haldiram's Mixture", 'brand': haldirams, 'category': snacks,
         'price': 50, 'discount_price': 45, 'weight': '250g', 'stock': 90, 'is_featured': True},
        
        # Amul
        {'name': 'Amul Butter', 'brand': amul, 'category': dairy,
         'price': 55, 'discount_price': 50, 'weight': '100g', 'stock': 200,
         'is_featured': True, 'rating_avg': 4.6, 'rating_count': 189, 'bought_count': 500},
        {'name': 'Amul Gold Full Cream Milk', 'brand': amul, 'category': dairy,
         'price': 31, 'weight': '500ml', 'stock': 100, 'is_featured': True},
        {'name': 'Amul Cheese Slices', 'brand': amul, 'category': dairy,
         'price': 115, 'discount_price': 105, 'weight': '200g', 'stock': 60},
        
        # Maggi
        {'name': 'Maggi 2-Minute Noodles (Masala)', 'brand': maggi, 'category': snacks,
         'price': 14, 'weight': '70g', 'stock': 500,
         'is_featured': True, 'rating_avg': 4.5, 'rating_count': 420, 'bought_count': 800},
        {'name': 'Maggi Family Pack 12 x 70g', 'brand': maggi, 'category': snacks,
         'price': 168, 'discount_price': 149, 'weight': '840g', 'stock': 80, 'is_featured': True},
        
        # Oreo
        {'name': 'Oreo Original Sandwich Cookies', 'brand': oreo, 'category': snacks,
         'price': 35, 'discount_price': 30, 'weight': '120g', 'stock': 150,
         'is_featured': True, 'rating_avg': 4.5, 'rating_count': 285},
        {'name': 'Oreo Double Stuff', 'brand': oreo, 'category': snacks,
         'price': 50, 'discount_price': 44, 'weight': '157g', 'stock': 80},
        
        # Cadbury
        {'name': 'Cadbury Dairy Milk', 'brand': cadbury, 'category': snacks,
         'price': 20, 'weight': '30g', 'stock': 200,
         'is_featured': True, 'rating_avg': 4.6, 'rating_count': 312, 'bought_count': 650},
        {'name': 'Cadbury 5 Star', 'brand': cadbury, 'category': snacks,
         'price': 20, 'weight': '40g', 'stock': 150},
        
        # Kurkure
        {'name': 'Kurkure Masala Munch', 'brand': kurkure, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '90g', 'stock': 120,
         'is_new_launch': True, 'is_featured': True},
        {'name': 'Kurkure Puffcorn Yummy Cheese', 'brand': kurkure, 'category': snacks,
         'price': 20, 'discount_price': 18, 'weight': '52g', 'stock': 100},
    ]
    
    created = 0
    for p in products:
        obj, new = Product.objects.get_or_create(
            name=p['name'],
            defaults={
                **p,
                'is_active': True,
                'delivery_eta': p.get('delivery_eta', 'Tomorrow'),
            }
        )
        if new:
            created += 1
    
    print(f'[OK] Products: {created} created, {len(products)-created} already existed')


def create_store_settings():
    """Create the store settings (key-value model)."""
    settings_data = {
        'store_name':             'Shivank Kirana Store',
        'store_phone':            '7599342112',
        'store_whatsapp':         '917599342112',
        'store_email':            'support@shivankkirana.com',
        'store_address':          '288, Main Market, Meerut - 250404',
        'store_lat':              '28.9845',
        'store_lng':              '77.7064',
        'upi_id':                 '7060169850@ptyes',
        'upi_name':               'Shivank So Om Pal',
        'free_delivery_threshold':'799',
        'base_delivery_charge':   '49',
        'distance_base_km':       '10',
        'distance_base_charge':   '99',
        'distance_increment_km':  '20',
        'distance_increment_charge': '50',
    }
    
    created = 0
    for key, value in settings_data.items():
        obj, new = StoreSettings.objects.get_or_create(key=key, defaults={'value': value})
        if new:
            created += 1
    print(f'[OK] Store settings: {created} created, {len(settings_data)-created} already existed')



def create_superuser():
    """Create default admin user if not exists."""
    from apps.accounts.models import CustomUser
    if not CustomUser.objects.filter(phone='9999999999').exists():
        user = CustomUser.objects.create_superuser(
            phone='9999999999',
            password='admin@kirana123',
            first_name='Shivank',
            last_name='So Om Pal',
        )
        user.is_admin = True
        user.save()
        print('[OK] Superuser created: phone=9999999999, password=admin@kirana123')
    else:
        print('[OK] Superuser already exists')


if __name__ == '__main__':
    import sys
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    print('\nSeeding Shivank Kirana Store database...\n')
    create_store_settings()
    create_categories()
    create_brands()
    create_sample_products()
    create_superuser()
    print('\nSeeding complete! Run: python manage.py runserver\n')

import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.products.models import Brand
from django.conf import settings

logo_dir = os.path.join(settings.BASE_DIR, 'Company_Brand_logo')
target_media_dir = os.path.join(settings.MEDIA_ROOT, 'brands')
os.makedirs(target_media_dir, exist_ok=True)

# File to Brand Name mapping
mapping = {
    "Amul_logo_PNG4.png": ["Amul"],
    "Ashirvaad logo.png": ["Aashirvaad", "Ashirvaad"],
    "Britannia.png": ["Britannia"],
    "Cadbury_Dairy_Milk_Logo_PNG2.png": ["Cadbury"],
    "Chupa_Chups_logo_PNG6.png": ["Chupa Chups"],
    "Colgate.png": ["Colgate"],
    "Haldiram_logo_PNG1.png": ["Haldiram's", "Haldiram", "Haldirams"],
    "Kit_kat_logo_PNG1.png": ["KitKat", "Kit Kat"],
    "Lays_logo_PNG3.png": ["Lay's", "Lays"],
    "Lifeboy.png": ["Lifebuoy", "Lifeboy"],
    "MMS_logo_PNG1.png": ["M&M's", "MMS"],
    "Maggi_logo_PNG4.png": ["Maggi"],
    "Nestle_logo_PNG4.png": ["Nestlé", "Nestle"],
    "Oreo_logo_PNG12.png": ["Oreo"],
    "Parle-Logo-PNG1.png": ["Parle"],
    "Surfexcel.png": ["Surf Excel", "Surfexcel"],
    "Tic_Tac_logo_PNG1.png": ["Tic Tac"],
    "dabur.png": ["Dabur"],
    "fortune.png": ["Fortune"],
    "tata.png": ["Tata", "TATA", "Tata Sampann"],
}

print("=== SYNCING BRAND LOGOS FROM Company_Brand_logo ===")
updated_count = 0

for fname, brand_names in mapping.items():
    src_file = os.path.join(logo_dir, fname)
    if not os.path.exists(src_file):
        print(f"File missing: {fname}")
        continue
    
    # Copy to media/brands/
    dest_name = fname.replace(' ', '_')
    dest_file = os.path.join(target_media_dir, dest_name)
    shutil.copy2(src_file, dest_file)
    rel_path = f"brands/{dest_name}"

    for bname in brand_names:
        brands = Brand.objects.filter(name__iexact=bname)
        if not brands.exists():
            # Try slug or contains
            brands = Brand.objects.filter(name__icontains=bname)
        
        for b in brands:
            b.logo = rel_path
            b.save(update_fields=['logo'])
            print(f"✓ Updated brand '{b.name}' -> {rel_path}")
            updated_count += 1

# Check all brands in DB
print("\n--- ALL BRANDS STATUS ---")
for b in Brand.objects.all():
    print(f"Brand: {b.name} | Logo: {b.logo.url if b.logo else 'NO LOGO'}")

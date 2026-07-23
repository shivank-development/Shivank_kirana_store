"""Home page view — Shivank Kirana Store."""
import os
import shutil
from django.shortcuts import render
from django.conf import settings
from apps.products.models import Product, Category, Brand


def auto_sync_brand_logos():
    """Auto-copies brand logo PNGs from Company_Brand_logo to media/brands/ and populates Brand.logo."""
    logo_dir = os.path.join(settings.BASE_DIR, 'Company_Brand_logo')
    target_media_dir = os.path.join(settings.MEDIA_ROOT, 'brands')
    if not os.path.exists(logo_dir):
        return

    os.makedirs(target_media_dir, exist_ok=True)

    file_brand_map = {
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
        "tata.png": ["Tata", "TATA"],
    }

    for fname, brand_names in file_brand_map.items():
        src_file = os.path.join(logo_dir, fname)
        if not os.path.exists(src_file):
            continue

        dest_name = fname.replace(' ', '_')
        dest_file = os.path.join(target_media_dir, dest_name)
        if not os.path.exists(dest_file):
            try:
                shutil.copy2(src_file, dest_file)
            except Exception:
                pass

        rel_path = f"brands/{dest_name}"
        for bname in brand_names:
            brands = Brand.objects.filter(name__icontains=bname)
            for b in brands:
                if not b.logo or not os.path.exists(os.path.join(settings.MEDIA_ROOT, str(b.logo))):
                    b.logo = rel_path
                    b.save(update_fields=['logo'])


def index(request):
    """Homepage — loads featured products, categories, and brands."""
    try:
        auto_sync_brand_logos()
    except Exception:
        pass

    # Categories (active, ordered)
    categories = Category.objects.filter(is_active=True).order_by('sort_order', 'name')[:12]
    
    # Featured products (is_featured=True or top sellers)
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True
    ).select_related('brand', 'category').order_by('-bought_count')[:20]
    
    # New launches
    new_products = Product.objects.filter(
        is_active=True, is_new_launch=True
    ).select_related('brand', 'category').order_by('-created_at')[:20]
    
    # All active brands (for slider)
    all_brands = Brand.objects.filter(is_active=True).order_by('sort_order', 'name')
    
    # Brand sections — top 6 brands with their products
    brand_sections = []
    top_brands = Brand.objects.filter(is_active=True).order_by('sort_order')[:6]
    for brand in top_brands:
        products = Product.objects.filter(
            brand=brand, is_active=True
        ).select_related('brand', 'category').order_by('-bought_count')[:10]
        if products.exists():
            brand_sections.append({'brand': brand, 'products': products})
    
    # Popular products (high-bought, for grid display on home page)
    popular_products = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').order_by('-bought_count', '-rating_avg')[:8]
    
    # User wishlist IDs (for showing filled heart)
    user_wishlist = set()
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        user_wishlist = set(WishlistItem.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True))
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_products': new_products,
        'popular_products': popular_products,
        'all_brands': all_brands,
        'brand_sections': brand_sections,
        'user_wishlist': user_wishlist,
    }
    
    return render(request, 'home/index.html', context)


def about_us(request):
    """About Us page."""
    return render(request, 'home/about_us.html')


def privacy_policy(request):
    """Privacy Policy page."""
    return render(request, 'home/privacy_policy.html')


def return_policy(request):
    """Return & Refund Policy page."""
    return render(request, 'home/return_policy.html')


def shipping_policy(request):
    """Shipping Policy page."""
    return render(request, 'home/shipping_policy.html')


def faqs(request):
    """FAQs page."""
    return render(request, 'home/faqs.html')


def contact_us(request):
    """Contact Us page."""
    return render(request, 'home/contact_us.html')

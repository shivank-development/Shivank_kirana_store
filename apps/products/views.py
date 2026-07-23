"""Products views — catalog, search, detail."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.products.models import Product, Category, Brand


def product_list(request):
    """Shop all products with filters."""
    qs = Product.objects.filter(is_active=True).select_related('brand', 'category')
    
    # Filters
    category_slug = request.GET.get('category')
    brand_slug    = request.GET.get('brand')
    filter_flag   = request.GET.get('filter')
    sort_by       = request.GET.get('sort', '-created_at')
    q             = request.GET.get('q', '')
    
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if brand_slug:
        qs = qs.filter(brand__slug=brand_slug)
    if filter_flag == 'new':
        qs = qs.filter(is_new_launch=True)
    if q:
        qs = qs.filter(name__icontains=q)
    
    sort_map = {
        'price_asc':  'discount_price',
        'price_desc': '-discount_price',
        'popular':    '-bought_count',
        'newest':     '-created_at',
        'rating':     '-rating_avg',
    }
    qs = qs.order_by(sort_map.get(sort_by, '-created_at'))
    
    # Pagination
    paginator   = Paginator(qs, 24)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True).order_by('sort_order')
    brands     = Brand.objects.filter(is_active=True).order_by('sort_order')
    
    # User wishlist
    user_wishlist = set()
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        user_wishlist = set(WishlistItem.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True))
    
    return render(request, 'products/product_list.html', {
        'page_obj':      page_obj,
        'products':      page_obj.object_list,
        'categories':    categories,
        'brands':        brands,
        'user_wishlist': user_wishlist,
        'current_cat':   category_slug,
        'current_brand': brand_slug,
        'current_sort':  sort_by,
        'search_query':  q,
    })


def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Related products
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).select_related('brand')[:8]
    
    # Reviews (once model added)
    reviews = product.reviews.filter(is_verified=True).order_by('-created_at')[:10] if hasattr(product, 'reviews') else []
    
    # Bulk pricing tiers ("Buy More Save More")
    bulk_prices = product.bulk_prices.all() if hasattr(product, 'bulk_prices') else []

    # Gallery images
    gallery_images = product.images.all().order_by('sort_order') if hasattr(product, 'images') else []

    # Rating average
    review_count = reviews.count() if hasattr(reviews, 'count') else len(reviews)
    rating_avg = (
        product.reviews.filter(is_verified=True).aggregate(
            avg=__import__('django.db.models', fromlist=['Avg']).Avg('rating')
        )['avg'] or 0
    ) if hasattr(product, 'reviews') else 0

    # User wishlist logic
    user_wishlist = set()
    in_wishlist = False
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
        user_wishlist = set(WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'products/product_detail.html', {
        'product':        product,
        'related':        related,
        'reviews':        reviews,
        'review_count':   review_count,
        'rating_avg':     round(rating_avg, 1),
        'bulk_prices':    bulk_prices,
        'gallery_images': gallery_images,
        'in_wishlist':    in_wishlist,
        'user_wishlist':  user_wishlist,
    })


def category_products(request, slug):
    """Products filtered by category slug."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    request.GET = request.GET.copy()
    request.GET['category'] = slug
    return product_list(request)


def brand_products(request, slug):
    """Products filtered by brand slug."""
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    request.GET = request.GET.copy()
    request.GET['brand'] = slug
    return product_list(request)

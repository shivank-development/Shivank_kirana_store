from django.shortcuts import render, get_object_or_404
from apps.products.models import Product, Brand


def brand_products(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True).select_related('category')
    
    user_wishlist = set()
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        user_wishlist = set(WishlistItem.objects.filter(
            user=request.user).values_list('product_id', flat=True))
    
    return render(request, 'products/product_list.html', {
        'products': products, 'brand': brand,
        'user_wishlist': user_wishlist, 'page_title': brand.name
    })

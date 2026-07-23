from django.shortcuts import render
from django.db.models import Q
from apps.products.models import Product, Category


def category_products(request, slug):
    """View products in a category with smart slug/keyword fallback."""
    category = Category.objects.filter(slug=slug, is_active=True).first()
    if not category:
        category = Category.objects.filter(slug__icontains=slug, is_active=True).first()
    if not category:
        category = Category.objects.filter(name__icontains=slug, is_active=True).first()

    if category:
        products = Product.objects.filter(category=category, is_active=True).select_related('brand', 'category')
        page_title = category.name
    else:
        # Keyword search fallback for snacks, chocolates, etc.
        keyword = slug.replace('-', ' ')
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=keyword) |
            Q(category__name__icontains=keyword)
        ).select_related('brand', 'category')
        page_title = keyword.title()

    user_wishlist = set()
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        user_wishlist = set(WishlistItem.objects.filter(
            user=request.user).values_list('product_id', flat=True))

    return render(request, 'products/product_list.html', {
        'products': products,
        'category': category,
        'user_wishlist': user_wishlist,
        'page_title': page_title
    })

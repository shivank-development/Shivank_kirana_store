from django.shortcuts import render
from django.http import JsonResponse
from apps.products.models import Product


def search_view(request):
    q = request.GET.get('q', '').strip()
    products = []
    if q:
        products = Product.objects.filter(
            is_active=True, name__icontains=q
        ).select_related('brand', 'category')[:50]
    
    user_wishlist = set()
    if request.user.is_authenticated:
        from apps.wishlist.models import WishlistItem
        user_wishlist = set(WishlistItem.objects.filter(
            user=request.user).values_list('product_id', flat=True))
    
    return render(request, 'search/search_results.html', {
        'products': products, 'query': q, 'user_wishlist': user_wishlist
    })


def search_api(request):
    """AJAX search autocomplete."""
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        products = Product.objects.filter(
            is_active=True, name__icontains=q
        ).select_related('brand')[:8]
        results = [{
            'name': p.name,
            'price': str(p.selling_price),
            'url': p.get_absolute_url(),
            'image': p.image_main.url if p.image_main else '',
        } for p in products]
    return JsonResponse({'results': results})

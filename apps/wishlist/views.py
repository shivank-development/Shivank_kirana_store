# Wishlist views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from apps.wishlist.models import WishlistItem
from apps.products.models import Product


@login_required
def wishlist_list(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product__brand', 'product__category')
    # Pass wishlist IDs so product_card heart icons render correctly
    user_wishlist = set(items.values_list('product_id', flat=True))
    return render(request, 'wishlist/wishlist_list.html', {
        'items': items,
        'user_wishlist': user_wishlist,
    })


def wishlist_count(request):
    """GET /wishlist/count/ — returns wishlist item count for the logged-in user."""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    count = WishlistItem.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})


@csrf_exempt
def toggle_wishlist(request, product_id):
    """AJAX: Toggle product in wishlist. CSRF handled via login session."""
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login to add to wishlist'}, status=401)
        
    try:
        product = Product.objects.get(pk=product_id, is_active=True)
        item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.delete()
            is_wishlisted = False
            msg = '💔 Removed from wishlist'
        else:
            is_wishlisted = True
            msg = '❤️ Added to wishlist!'
            
        return JsonResponse({'success': True, 'is_wishlisted': is_wishlisted, 'message': msg})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)

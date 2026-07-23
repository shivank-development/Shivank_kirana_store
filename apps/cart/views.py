from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
import json


def cart_view(request):
    """Cart page."""
    cart  = None
    items = []
    applied_coupon_code = None
    coupon_discount = 0.0
    
    from apps.orders.models import Coupon
    try:
        available_coupons = list(Coupon.objects.filter(is_active=True).order_by('-created_at'))
    except Exception:
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM coupons WHERE discount_value IS NULL OR discount_value = ''")
                cursor.execute("SELECT id, discount_value FROM coupons")
                rows = cursor.fetchall()
                for c_id, disc in rows:
                    try:
                        float(disc)
                    except Exception:
                        cursor.execute(f"DELETE FROM coupons WHERE id = {int(c_id)}")
        except Exception:
            pass
        try:
            available_coupons = list(Coupon.objects.filter(is_active=True).order_by('-created_at'))
        except Exception:
            available_coupons = []

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items   = list(cart.items.select_related('product__brand').all())

        code = request.session.get('applied_coupon')
        if code:
            cp = Coupon.objects.filter(code=code, is_active=True).first()
            if cp:
                disc = cp.calculate_discount(cart.subtotal)
                if disc > 0:
                    applied_coupon_code = cp.code
                    coupon_discount = float(disc)
                else:
                    request.session.pop('applied_coupon', None)
                    request.session.pop('coupon_discount', None)

    subtotal = float(cart.subtotal) if cart else 0.0
    delivery_charge = float(cart.delivery_charge) if cart else 0.0
    grand_total = max(0.0, subtotal + delivery_charge - coupon_discount) if cart else 0.0

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'cart_count': cart.item_count if cart else 0,
        'available_coupons': available_coupons,
        'applied_coupon_code': applied_coupon_code,
        'coupon_discount': coupon_discount,
        'grand_total': grand_total,
    })


@csrf_exempt
def add_to_cart(request):
    """AJAX: Add product to cart."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'})
    
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login'}, status=401)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity   = int(data.get('quantity', 1))
        
        product = Product.objects.get(pk=product_id, is_active=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity = min(item.quantity + quantity, product.stock)
        else:
            item.quantity = quantity
        item.save()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'subtotal': float(cart.subtotal),
            'total_mrp': float(cart.total_mrp),
            'savings': float(cart.savings),
            'delivery_charge': float(cart.delivery_charge),
            'total': float(cart.total),
            'message': f'{product.name} added to cart',
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def remove_from_cart(request, item_id):
    """AJAX: Remove item from cart."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)
    
    CartItem.objects.filter(pk=item_id, cart__user=request.user).delete()
    cart = Cart.objects.filter(user=request.user).first()
    return JsonResponse({
        'success': True, 
        'cart_count': cart.item_count if cart else 0,
        'subtotal': float(cart.subtotal) if cart else 0,
        'total_mrp': float(cart.total_mrp) if cart else 0,
        'savings': float(cart.savings) if cart else 0,
        'delivery_charge': float(cart.delivery_charge) if cart else 0,
        'total': float(cart.total) if cart else 0,
    })


@csrf_exempt
def update_cart(request, item_id):
    """AJAX: Update cart item quantity."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)
    
    try:
        data     = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        item     = CartItem.objects.get(pk=item_id, cart__user=request.user)
        
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = min(quantity, item.product.stock)
            item.save()
        
        cart = Cart.objects.filter(user=request.user).first()
        return JsonResponse({
            'success': True, 
            'cart_count': cart.item_count if cart else 0,
            'item_subtotal': float(item.subtotal) if quantity > 0 else 0,
            'subtotal': float(cart.subtotal) if cart else 0,
            'total_mrp': float(cart.total_mrp) if cart else 0,
            'savings': float(cart.savings) if cart else 0,
            'delivery_charge': float(cart.delivery_charge) if cart else 0,
            'total': float(cart.total) if cart else 0,
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)


@csrf_exempt
def update_cart_ajax(request):
    """AJAX: Update cart item via body {item_id, delta} — used by cart drawer."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)
    try:
        data    = json.loads(request.body)
        item_id = data.get('item_id')
        delta   = int(data.get('delta', 0))
        item    = CartItem.objects.get(pk=item_id, cart__user=request.user)
        new_qty = item.quantity + delta
        if new_qty <= 0:
            item.delete()
        else:
            item.quantity = min(new_qty, item.product.stock)
            item.save()
        cart = Cart.objects.filter(user=request.user).first()
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count if cart else 0,
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def remove_cart_ajax(request):
    """AJAX: Remove cart item via body {item_id} — used by cart drawer."""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False}, status=401)
    try:
        data    = json.loads(request.body)
        item_id = data.get('item_id')
        CartItem.objects.filter(pk=item_id, cart__user=request.user).delete()
        cart = Cart.objects.filter(user=request.user).first()
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count if cart else 0,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def cart_count(request):
    """GET /cart/count/ — returns cart item count."""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    cart = Cart.objects.filter(user=request.user).first()
    return JsonResponse({'count': cart.item_count if cart else 0})


def cart_data(request):
    """GET /cart/data/ — returns full cart contents for drawer rendering."""
    if not request.user.is_authenticated:
        return JsonResponse({'items': [], 'total': 0, 'total_items': 0})

    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'items': [], 'total': 0, 'total_items': 0})

    items_data = []
    for item in cart.items.select_related('product').all():
        product = item.product
        image_url = request.build_absolute_uri(product.image_main.url) if product.image_main else ''
        items_data.append({
            'id': item.id,
            'name': product.name,
            'image': image_url,
            'price': float(product.selling_price),
            'quantity': item.quantity,
            'subtotal': float(item.subtotal),
        })

    return JsonResponse({
        'items': items_data,
        'total': float(cart.total),
        'subtotal': float(cart.subtotal),
        'delivery_charge': float(cart.delivery_charge),
        'total_items': cart.item_count,
    })


@csrf_exempt
def apply_coupon(request):
    """AJAX: Apply coupon code to user session."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login to apply coupons'}, status=401)

    from apps.orders.models import Coupon
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        if not code:
            return JsonResponse({'success': False, 'message': 'Please enter a coupon code'})

        coupon = Coupon.objects.filter(code=code, is_active=True).first()
        if not coupon:
            return JsonResponse({'success': False, 'message': f'Coupon "{code}" is invalid or expired'})

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or cart.item_count == 0:
            return JsonResponse({'success': False, 'message': 'Your cart is empty'})

        if coupon.min_order_amount and cart.subtotal < coupon.min_order_amount:
            return JsonResponse({
                'success': False,
                'message': f'Minimum order of ₹{coupon.min_order_amount} required for coupon "{code}"'
            })

        discount = coupon.calculate_discount(cart.subtotal)
        if discount <= 0:
            return JsonResponse({'success': False, 'message': 'Coupon conditions not met for this order'})

        request.session['applied_coupon'] = coupon.code
        request.session['coupon_discount'] = float(discount)

        subtotal = float(cart.subtotal)
        delivery = float(cart.delivery_charge)
        disc_val = float(discount)
        grand_total = max(0.0, subtotal + delivery - disc_val)

        return JsonResponse({
            'success': True,
            'message': f'🎉 Coupon "{coupon.code}" applied! You saved ₹{disc_val:.2f}',
            'coupon_code': coupon.code,
            'coupon_discount': disc_val,
            'subtotal': subtotal,
            'delivery_charge': delivery,
            'grand_total': grand_total,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def remove_coupon(request):
    """AJAX: Remove coupon code from user session."""
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=400)

    request.session.pop('applied_coupon', None)
    request.session.pop('coupon_discount', None)

    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    subtotal = float(cart.subtotal) if cart else 0.0
    delivery = float(cart.delivery_charge) if cart else 0.0

    return JsonResponse({
        'success': True,
        'message': 'Coupon removed',
        'coupon_discount': 0,
        'subtotal': subtotal,
        'delivery_charge': delivery,
        'grand_total': subtotal + delivery,
    })

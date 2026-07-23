"""Checkout views — full checkout flow with UPI/COD."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal


def _get_cart_context(user, request=None):
    """Build cart context dict for checkout and cart pages."""
    from apps.cart.models import Cart
    from apps.orders.models import StoreSettings, Coupon
    
    # Fetch dynamic settings from database
    def get_setting(key, default, cast_type=float):
        val = StoreSettings.objects.filter(key=key).first()
        if val:
            try: return cast_type(val.value)
            except: pass
        return default

    FREE_DELIVERY_THRESHOLD = get_setting('free_delivery_threshold', 799)
    BASE_DELIVERY_CHARGE    = get_setting('base_delivery_charge', 49)

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

    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return {
            'cart': None, 'items': [], 'cart_items': [],
            'subtotal': 0, 'delivery_charge': 0, 'coupon_discount': 0, 'total': 0, 'cart_count': 0,
            'available_coupons': available_coupons, 'applied_coupon_code': None,
        }

    items = list(cart.items.select_related('product__brand').all())

    subtotal         = sum(i.subtotal for i in items)
    delivery_charge  = Decimal('0') if subtotal >= Decimal(str(FREE_DELIVERY_THRESHOLD)) else Decimal(str(BASE_DELIVERY_CHARGE))
    
    # Coupon handling
    applied_coupon_code = request.session.get('applied_coupon') if request else None
    coupon_discount = Decimal('0')

    if applied_coupon_code:
        cp = Coupon.objects.filter(code=applied_coupon_code, is_active=True).first()
        if cp:
            disc = cp.calculate_discount(subtotal)
            if disc > 0:
                coupon_discount = disc
            elif request:
                request.session.pop('applied_coupon', None)
                request.session.pop('coupon_discount', None)
                applied_coupon_code = None

    total = max(Decimal('0'), subtotal + delivery_charge - coupon_discount)

    return {
        'cart': cart,
        'items': items,
        'cart_items': items,        # alias used in checkout template
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'coupon_discount': coupon_discount,
        'applied_coupon_code': applied_coupon_code,
        'total': total,
        'cart_count': cart.item_count,
        'available_coupons': available_coupons,
        'upi_id': get_setting('upi_id', '7060169850@ptyes', cast_type=str),
    }


@login_required(login_url='/auth/login/')
def checkout_view(request):
    """Render full checkout page."""
    ctx = _get_cart_context(request.user, request=request)
    if not ctx['items']:
        messages.warning(request, 'Your cart is empty. Add items before checking out.')
        return redirect('/cart/')
    return render(request, 'checkout/checkout.html', ctx)


@login_required(login_url='/auth/login/')
def place_order(request):
    """Handle order placement from checkout form."""
    if request.method != 'POST':
        return redirect('/checkout/')

    from apps.cart.models import Cart
    from apps.orders.models import Order, OrderItem, Coupon

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.item_count == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('/cart/')

    # Collect form data
    full_name      = request.POST.get('full_name', '').strip()
    phone          = request.POST.get('phone', '').strip()
    address        = request.POST.get('address', '').strip()
    city           = request.POST.get('city', 'Meerut').strip()
    pincode        = request.POST.get('pincode', '').strip()
    instructions   = request.POST.get('instructions', '').strip()
    payment_method = request.POST.get('payment_method', 'upi')
    utr_number     = request.POST.get('utr_number', '').strip()
    cod_advance    = request.POST.get('cod_advance_utr', '').strip()

    # Basic validation
    if not all([full_name, phone, address, pincode]):
        messages.error(request, 'Please fill in all required delivery fields.')
        return redirect('/checkout/')

    # Check deliverable pincodes
    from apps.delivery.models import DeliveryPincode
    active_pincodes = DeliveryPincode.objects.filter(is_active=True)
    if active_pincodes.exists():
        if not active_pincodes.filter(pincode=pincode).exists():
            messages.error(request, f'Delivery is not available in pincode "{pincode}". Not deliver in the pincode.')
            return redirect('/checkout/')

    if payment_method == 'upi' and not utr_number:
        messages.error(request, 'Please enter your UPI UTR / Transaction ID.')
        return redirect('/checkout/')

    if payment_method == 'cod' and not cod_advance:
        messages.error(request, 'Please enter the ₹49 advance payment UTR.')
        return redirect('/checkout/')

    # Fetch dynamic settings
    from apps.orders.models import StoreSettings
    def get_setting(key, default, cast_type=float):
        val = StoreSettings.objects.filter(key=key).first()
        if val:
            try: return cast_type(val.value)
            except: pass
        return default
        
    FREE_THRESHOLD   = Decimal(str(get_setting('free_delivery_threshold', 799)))
    BASE_DELIVERY    = Decimal(str(get_setting('base_delivery_charge', 49)))

    # Build totals
    items            = list(cart.items.select_related('product').all())
    subtotal         = sum(item.product.selling_price * item.quantity for item in items)
    delivery_charge  = Decimal('0') if subtotal >= FREE_THRESHOLD else BASE_DELIVERY
    
    # Coupon calculation
    applied_coupon_code = request.session.get('applied_coupon')
    coupon_discount = Decimal('0')
    if applied_coupon_code:
        cp = Coupon.objects.filter(code=applied_coupon_code, is_active=True).first()
        if cp:
            disc = cp.calculate_discount(subtotal)
            if disc > 0:
                coupon_discount = disc
                cp.used_count += 1
                cp.save()

    total = max(Decimal('0'), subtotal + delivery_charge - coupon_discount)

    # Create the Order
    delivery_address = f"{full_name}, {address}, {city} - {pincode}"
    if instructions:
        delivery_address += f" ({instructions})"

    try:
        import uuid
        order_num = f"SKS{uuid.uuid4().hex[:8].upper()}"

        # Build delivery info into notes (address FK is optional since we take text)
        delivery_note = (
            f"Name: {full_name} | Phone: {phone}\n"
            f"Address: {address}, {city} - {pincode}"
        )
        if instructions:
            delivery_note += f"\nInstructions: {instructions}"

        utr = utr_number or cod_advance

        order = Order.objects.create(
            user               = request.user,
            order_number       = order_num,
            payment_method     = payment_method.upper(),   # model expects 'UPI' or 'COD'
            subtotal           = subtotal,
            delivery_charge    = delivery_charge,
            coupon_discount    = coupon_discount,
            total_amount       = total,
            status             = 'placed',
            payment_status     = 'pending',
            upi_transaction_id = utr,
            notes              = delivery_note,
        )

        # Clear coupon from session
        request.session.pop('applied_coupon', None)
        request.session.pop('coupon_discount', None)

        # Create order items
        for item in items:
            OrderItem.objects.create(
                order         = order,
                product       = item.product,
                quantity      = item.quantity,
                unit_price    = item.product.selling_price,
                total_price   = item.product.selling_price * item.quantity,
            )

        # Clear the cart
        cart.items.all().delete()

        messages.success(request, f'Order {order.order_number} placed successfully!')
        return redirect(f'/orders/success/{order.id}/')

    except Exception as e:
        messages.error(request, f'Order failed: {str(e)}')
        return redirect('/checkout/')


def check_pincode_api(request):
    pincode = request.GET.get('pincode', '').strip()
    from apps.delivery.models import DeliveryPincode
    from django.http import JsonResponse
    
    if not pincode or len(pincode) < 6:
        return JsonResponse({'deliverable': False, 'message': ''})

    active_pincodes = DeliveryPincode.objects.filter(is_active=True)
    if not active_pincodes.exists():
        return JsonResponse({'deliverable': True, 'message': '✅ Delivery Available'})

    if active_pincodes.filter(pincode=pincode).exists():
        obj = active_pincodes.filter(pincode=pincode).first()
        area = f" ({obj.area_name})" if obj.area_name else ""
        return JsonResponse({'deliverable': True, 'message': f'✅ Delivery Available{area}!'})
    else:
        return JsonResponse({'deliverable': False, 'message': '❌ Not deliver in the pincode'})


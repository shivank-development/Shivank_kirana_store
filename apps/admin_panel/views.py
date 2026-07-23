from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages

from apps.orders.models import Order
from apps.products.models import Product, Brand
from apps.accounts.models import CustomUser
from .forms import BrandForm, ProductForm


@staff_member_required
def admin_dashboard(request):
    context = {
        'total_orders':   Order.objects.count(),
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_users':    CustomUser.objects.filter(role='customer').count(),
        'pending_orders': Order.objects.filter(status='placed').count(),
        'recent_orders':  Order.objects.select_related('user').order_by('-placed_at')[:10],
        'low_stock':      Product.objects.filter(stock__lte=5, is_active=True).select_related('category')[:10],
    }
    return render(request, 'admin_panel/dashboard.html', context)



# ==========================================
# BRAND CRUD
# ==========================================
@staff_member_required
def brand_list(request):
    brands_list = Brand.objects.all().order_by('sort_order', 'name')
    paginator = Paginator(brands_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/brand_list.html', {'page_obj': page_obj})

@staff_member_required
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand created successfully.")
            return redirect('admin_panel:brand_list')
    else:
        form = BrandForm()
    return render(request, 'admin_panel/brand_form.html', {'form': form, 'title': 'Create Brand'})

@staff_member_required
def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand updated successfully.")
            return redirect('admin_panel:brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'admin_panel/brand_form.html', {'form': form, 'title': 'Edit Brand'})

@staff_member_required
def brand_delete(request, pk):
    brand = Brand.objects.filter(pk=pk).first()
    if not brand:
        messages.info(request, "Brand already deleted or does not exist.")
        return redirect('admin_panel:brand_list')
    
    brand.delete()
    messages.success(request, "Brand deleted successfully.")
    return redirect('admin_panel:brand_list')


# ==========================================
# PRODUCT CRUD
# ==========================================
@staff_member_required
def product_list(request):
    q = request.GET.get('q', '')
    qs = Product.objects.all().select_related('brand', 'category').order_by('-created_at')
    if q:
        qs = qs.filter(name__icontains=q)
        
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_panel/product_list.html', {'page_obj': page_obj, 'search_query': q})

from .forms import BrandForm, ProductForm, ProductImageFormSet, BulkPricingFormSet

@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
            pricing_formset = BulkPricingFormSet(request.POST, instance=product)
            # Gallery images are optional — save independently if valid
            if image_formset.is_valid():
                image_formset.save()
            if pricing_formset.is_valid():
                pricing_formset.save()
            messages.success(request, "Product created successfully.")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet()
        pricing_formset = BulkPricingFormSet()
    
    return render(request, 'admin_panel/product_form.html', {
        'form': form, 
        'image_formset': image_formset,
        'pricing_formset': pricing_formset,
        'title': 'Create Product'
    })

@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        pricing_formset = BulkPricingFormSet(request.POST, instance=product)
        
        if form.is_valid() and image_formset.is_valid() and pricing_formset.is_valid():
            form.save()
            image_formset.save()
            pricing_formset.save()
            messages.success(request, "Product updated successfully.")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)
        pricing_formset = BulkPricingFormSet(instance=product)
        
    return render(request, 'admin_panel/product_form.html', {
        'form': form, 
        'image_formset': image_formset,
        'pricing_formset': pricing_formset,
        'title': 'Edit Product'
    })

@staff_member_required
def product_delete(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        messages.info(request, "Product already deleted or does not exist.")
        return redirect('admin_panel:product_list')
    
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('admin_panel:product_list')


# ==========================================
# REVIEWS MANAGEMENT
# ==========================================
from apps.products.models import ProductReview

@staff_member_required
def review_list(request):
    reviews = ProductReview.objects.select_related('product', 'user').order_by('-created_at')
    
    paginator = Paginator(reviews, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/review_list.html', {'page_obj': page_obj})

@staff_member_required
def review_toggle_verify(request, pk):
    if request.method == 'POST':
        review = get_object_or_404(ProductReview, pk=pk)
        review.is_verified = not review.is_verified
        review.save()
        messages.success(request, f"Review status updated for {review.product.name}")
    return redirect('admin_panel:review_list')

@staff_member_required
def review_delete(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect('admin_panel:review_list')
    return render(request, 'admin_panel/confirm_delete.html', {'object': f"Review by {review.user.full_name}", 'type': 'Review', 'cancel_url': 'admin_panel:review_list'})


# ==========================================
# ORDERS MANAGEMENT
# ==========================================

@staff_member_required
def order_list(request):
    from django.db.models import Q

    q              = request.GET.get('q', '').strip()
    status_filter  = request.GET.get('status', '').strip()
    method_filter  = request.GET.get('method', '').strip()

    qs = Order.objects.select_related('user').order_by('-placed_at')

    if q:
        qs = qs.filter(
            Q(order_number__icontains=q) |
            Q(user__full_name__icontains=q) |
            Q(user__phone_number__icontains=q) |
            Q(user__email__icontains=q)
        )

    if status_filter:
        qs = qs.filter(status=status_filter)

    if method_filter:
        qs = qs.filter(payment_method__iexact=method_filter)

    paginator = Paginator(qs, 20)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'admin_panel/order_list.html', {
        'page_obj':        page_obj,
        'search_query':    q,
        'status_filter':   status_filter,
        'method_filter':   method_filter,
        'status_choices':  Order.STATUS_CHOICES,
        'payment_methods': Order.PAYMENT_METHOD_CHOICES,
    })


@staff_member_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('user', 'address', 'delivery_boy'), pk=pk)
    items = order.items.select_related('product').all()
    
    # We might need delivery boys for assignment
    delivery_boys = CustomUser.objects.filter(role='delivery_boy', is_active=True)
    
    return render(request, 'admin_panel/order_detail.html', {
        'order': order,
        'items': items,
        'delivery_boys': delivery_boys,
        'status_choices': Order.STATUS_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
    })

@staff_member_required
def order_update(request, pk):
    from apps.orders.models import Payment, DeliveryTracking
    
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')
        delivery_boy_id = request.POST.get('delivery_boy')
        notes = request.POST.get('admin_notes', '')

        from apps.notifications.models import Notification

        if new_status and new_status != order.status:
            order.status = new_status
            
            # Simple timestamp updates based on status
            from django.utils import timezone
            now = timezone.now()
            if new_status == 'confirmed' and not order.confirmed_at:
                order.confirmed_at = now
            elif new_status == 'packed' and not order.packed_at:
                order.packed_at = now
            elif new_status == 'out_for_delivery' and not order.out_for_delivery_at:
                order.out_for_delivery_at = now
            elif new_status == 'delivered' and not order.delivered_at:
                order.delivered_at = now
            elif new_status == 'cancelled' and not order.cancelled_at:
                order.cancelled_at = now
                
            # Sync tracking status
            if hasattr(order, 'tracking'):
                order.tracking.status = new_status
                order.tracking.save()

            # Notify Customer
            try:
                Notification.objects.create(
                    user=order.user,
                    title=f"Order #{order.order_number} Update 📦",
                    message=f"Your order status is now '{order.get_status_display()}'.",
                    notif_type="order",
                    action_url=f"/orders/{order.id}/"
                )
            except Exception:
                pass

        if new_payment_status and new_payment_status != order.payment_status:
            order.payment_status = new_payment_status
            # Sync Payment table
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'payment_method': order.payment_method,
                    'amount': order.total_amount,
                    'upi_txn_id': order.upi_transaction_id,
                }
            )
            payment.status = new_payment_status
            from django.utils import timezone
            payment.admin_action = 'approved' if new_payment_status == 'received' else ('rejected' if new_payment_status in ['rejected', 'failed'] else '')
            payment.admin_action_by = request.user
            payment.admin_action_at = timezone.now()
            payment.save()

            # Notify Customer
            try:
                Notification.objects.create(
                    user=order.user,
                    title=f"Payment Status Update 💳",
                    message=f"Payment status for Order #{order.order_number} is now '{order.get_payment_status_display()}'.",
                    notif_type="payment",
                    action_url=f"/orders/{order.id}/"
                )
            except Exception:
                pass
            
        if delivery_boy_id:
            try:
                boy = CustomUser.objects.get(pk=delivery_boy_id, role='delivery_boy')
                order.delivery_boy = boy
                
                # Sync DeliveryTracking
                tracking, created = DeliveryTracking.objects.get_or_create(order=order)
                tracking.delivery_boy = boy
                tracking.status = order.status
                if order.address:
                    tracking.customer_lat = order.address.latitude
                    tracking.customer_lng = order.address.longitude
                tracking.distance_km = order.distance_km
                tracking.save()

                # Notify Customer
                try:
                    Notification.objects.create(
                        user=order.user,
                        title=f"Delivery Partner Assigned 🚴",
                        message=f"{boy.full_name} has been assigned to deliver your order #{order.order_number}.",
                        notif_type="delivery",
                        action_url=f"/orders/{order.id}/"
                    )
                except Exception:
                    pass
                
            except CustomUser.DoesNotExist:
                pass
        elif delivery_boy_id == '': # Specifically clear it
            order.delivery_boy = None
            if hasattr(order, 'tracking'):
                order.tracking.delivery_boy = None
                order.tracking.save()

        if notes:
            # Append notes
            if order.notes:
                order.notes += f"\n\n[Admin Note]: {notes}"
            else:
                order.notes = f"[Admin Note]: {notes}"

        order.save()
        messages.success(request, f"Order {order.order_number} updated successfully.")
        
    return redirect('admin_panel:order_detail', pk=pk)

@staff_member_required
def order_toggle_cod(request, pk):
    """Toggle COD call confirmed status quickly from the list view."""
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        order.cod_call_confirmed = not order.cod_call_confirmed
        order.save()
        status_text = "confirmed" if order.cod_call_confirmed else "unconfirmed"
        messages.success(request, f"COD call marked as {status_text} for {order.order_number}")
    return redirect(request.META.get('HTTP_REFERER', 'admin_panel:order_list'))


# ==========================================
# SETTINGS & COUPONS
# ==========================================

@staff_member_required
def store_settings_view(request):
    from apps.orders.models import StoreSettings
    
    # Define the keys we expect to handle in this UI
    expected_keys = [
        'store_name', 'store_phone', 'store_email', 'store_address',
        'upi_id', 'upi_name', 'store_lat', 'store_lng',
        'free_delivery_threshold', 'base_delivery_charge',
        'distance_base_charge', 'distance_increment_charge',
        'distance_base_km', 'distance_increment_km'
    ]
    
    if request.method == 'POST':
        for key in expected_keys:
            val = request.POST.get(key)
            if val is not None:
                # Update or create the setting
                setting, created = StoreSettings.objects.get_or_create(key=key)
                setting.value = val
                setting.save()
        messages.success(request, "Store settings updated successfully!")
        return redirect('admin_panel:store_settings')
        
    # Get current settings
    settings_dict = {}
    for setting in StoreSettings.objects.all():
        settings_dict[setting.key] = setting.value
        
    return render(request, 'admin_panel/store_settings.html', {'settings': settings_dict})

@staff_member_required
def coupon_list(request):
    from apps.orders.models import Coupon
    from decimal import Decimal, InvalidOperation
    from django.db import connection

    def clean_invalid_rows():
        try:
            with connection.cursor() as cursor:
                # 1. Remove empty/null strings
                cursor.execute("DELETE FROM coupons WHERE discount_value IS NULL OR discount_value = ''")
                # 2. Check for non-numeric text values and purge bad records
                cursor.execute("SELECT id, discount_value, min_order_amount FROM coupons")
                rows = cursor.fetchall()
                for c_id, disc, min_ord in rows:
                    is_bad = False
                    try:
                        if disc is not None: Decimal(str(disc))
                        if min_ord is not None: Decimal(str(min_ord))
                    except Exception:
                        is_bad = True
                    
                    if is_bad:
                        cursor.execute(f"DELETE FROM coupons WHERE id = {int(c_id)}")
        except Exception:
            pass

    # Run cleanup once on page load to ensure data integrity
    clean_invalid_rows()

    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        discount_type = request.POST.get('discount_type', 'percent').strip()
        disc_val_raw = request.POST.get('discount_value', '0').strip()
        min_ord_raw = request.POST.get('min_order_amount', '0').strip()

        try:
            disc_val = Decimal(disc_val_raw)
        except Exception:
            disc_val = Decimal('0')

        try:
            min_ord = Decimal(min_ord_raw) if min_ord_raw else Decimal('0')
        except Exception:
            min_ord = Decimal('0')

        if code and disc_val > 0:
            try:
                coupon, created = Coupon.objects.update_or_create(
                    code=code,
                    defaults={
                        'discount_type': discount_type,
                        'discount_value': disc_val,
                        'min_order_amount': min_ord,
                        'is_active': True
                    }
                )
                action_str = "created" if created else "updated"
                messages.success(request, f"Coupon {code} {action_str} successfully!")
            except Exception as e:
                messages.error(request, f"Error saving coupon: {e}")
        else:
            messages.error(request, "Please enter a valid coupon code and positive discount value.")
        return redirect('admin_panel:coupon_list')

    try:
        coupons = list(Coupon.objects.all().order_by('-created_at'))
    except Exception:
        clean_invalid_rows()
        try:
            coupons = list(Coupon.objects.all().order_by('-created_at'))
        except Exception:
            coupons = []
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, code, discount_type, discount_value, min_order_amount, is_active FROM coupons")
                    for r in cursor.fetchall():
                        c_id, c_code, c_type, c_disc, c_min, c_act = r
                        try:
                            d_val = Decimal(str(c_disc)) if c_disc else Decimal('0')
                            m_val = Decimal(str(c_min)) if c_min else Decimal('0')
                            coupons.append(Coupon(
                                id=c_id,
                                code=c_code,
                                discount_type=c_type,
                                discount_value=d_val,
                                min_order_amount=m_val,
                                is_active=bool(c_act)
                            ))
                        except Exception:
                            pass
            except Exception:
                pass

    active_count = sum(1 for c in coupons if c.is_active)
    return render(request, 'admin_panel/coupon_list.html', {
        'coupons': coupons,
        'active_count': active_count,
    })

@staff_member_required
def coupon_delete(request, pk):
    from apps.orders.models import Coupon
    from django.db import connection

    if request.method == 'POST':
        try:
            coupon = Coupon.objects.filter(pk=pk).first()
            if coupon:
                coupon.delete()
            else:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM coupons WHERE id = %s", [pk])
        except Exception:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM coupons WHERE id = %s", [pk])

        messages.success(request, "Coupon deleted successfully!")
        return redirect('admin_panel:coupon_list')

    try:
        coupon = Coupon.objects.filter(pk=pk).first()
        code = coupon.code if coupon else f"#{pk}"
    except Exception:
        code = f"#{pk}"
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT code FROM coupons WHERE id = %s", [pk])
                row = cursor.fetchone()
                if row and row[0]:
                    code = row[0]
        except Exception:
            pass

    return render(request, 'admin_panel/confirm_delete.html', {
        'object': f"Coupon {code}",
        'type': 'Coupon',
        'cancel_url': 'admin_panel:coupon_list'
    })


# ==========================================
# PAYMENTS MANAGEMENT
# ==========================================

@staff_member_required
def payments_manage(request):
    """★ Approve/Reject UPI payments, view UTR."""
    from apps.orders.models import Payment
    
    status_filter = request.GET.get('status', '')
    method_filter = request.GET.get('method', '')
    
    qs = Payment.objects.select_related('order', 'order__user').order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if method_filter:
        qs = qs.filter(payment_method=method_filter)
    
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Summary counts
    pending_count  = Payment.objects.filter(status='pending').count()
    received_count = Payment.objects.filter(status='received').count()
    rejected_count = Payment.objects.filter(status='rejected').count()
    
    return render(request, 'admin_panel/payments_manage.html', {
        'page_obj': page_obj,
        'pending_count': pending_count,
        'received_count': received_count,
        'rejected_count': rejected_count,
        'status_filter': status_filter,
        'method_filter': method_filter,
    })


@staff_member_required
def payment_action(request, pk):
    """Approve or reject a payment."""
    from apps.orders.models import Payment
    from django.utils import timezone
    
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')  # 'approve' or 'reject'
        notes  = request.POST.get('notes', '')
        
        if action == 'approve':
            payment.status = 'received'
            payment.admin_action = 'approved'
            payment.order.payment_status = 'received'
            if payment.order.status == 'placed':
                payment.order.status = 'confirmed'
                payment.order.confirmed_at = timezone.now()
            payment.order.save()
            messages.success(request, f"Payment for {payment.order.order_number} APPROVED ✓")
        elif action == 'reject':
            payment.status = 'rejected'
            payment.admin_action = 'rejected'
            payment.order.payment_status = 'rejected'
            payment.order.save()
            messages.warning(request, f"Payment for {payment.order.order_number} REJECTED ✗")
        
        payment.admin_action_by  = request.user
        payment.admin_action_at  = timezone.now()
        payment.admin_notes      = notes
        payment.save()
    
    return redirect('admin_panel:payments_manage')


# ==========================================
# CATEGORIES MANAGEMENT
# ==========================================

@staff_member_required
def categories_manage(request):
    """CRUD categories."""
    from apps.products.models import Category
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            name = request.POST.get('name', '').strip()
            if name:
                from django.utils.text import slugify
                Category.objects.get_or_create(
                    slug=slugify(name),
                    defaults={'name': name, 'is_active': True}
                )
                messages.success(request, f"Category '{name}' created.")
        elif action == 'delete':
            cat_id = request.POST.get('cat_id')
            Category.objects.filter(pk=cat_id).delete()
            messages.success(request, "Category deleted.")
        elif action == 'toggle':
            cat_id = request.POST.get('cat_id')
            cat = get_object_or_404(Category, pk=cat_id)
            cat.is_active = not cat.is_active
            cat.save()
        return redirect('admin_panel:categories_manage')
    
    from apps.products.models import Category
    categories = Category.objects.order_by('sort_order', 'name')
    
    return render(request, 'admin_panel/categories_manage.html', {
        'categories': categories,
    })


# ==========================================
# CUSTOMERS MANAGEMENT
# ==========================================

@staff_member_required
def customers_manage(request):
    """Customer list with order history."""
    q = request.GET.get('q', '')
    qs = CustomUser.objects.filter(role='customer').order_by('-date_joined')
    if q:
        qs = qs.filter(full_name__icontains=q) | CustomUser.objects.filter(
            role='customer', phone__icontains=q)
    
    # Annotate with order count
    from django.db.models import Count, Sum
    qs = CustomUser.objects.filter(role='customer').annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_amount'),
    ).order_by('-date_joined')
    if q:
        qs = qs.filter(full_name__icontains=q)
    
    paginator = Paginator(qs, 25)
    page_obj  = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'admin_panel/customers_manage.html', {
        'page_obj': page_obj,
        'search_query': q,
        'total_customers': CustomUser.objects.filter(role='customer').count(),
    })


# ==========================================
# DELIVERY MANAGEMENT
# ==========================================

@staff_member_required
def delivery_manage(request):
    """Delivery boys management + live tracking overview."""
    from apps.orders.models import DeliveryBoy, DeliveryTracking

    delivery_boys = CustomUser.objects.filter(
        role='delivery_boy'
    ).select_related('delivery_profile').order_by('full_name')

    active_deliveries = Order.objects.filter(
        status='out_for_delivery'
    ).select_related('user', 'delivery_boy', 'tracking')

    pending_assignment = Order.objects.filter(
        status='confirmed', delivery_boy__isnull=True
    ).select_related('user')[:20]

    return render(request, 'admin_panel/delivery_manage.html', {
        'delivery_boys': delivery_boys,
        'active_deliveries': active_deliveries,
        'pending_assignment': pending_assignment,
        'total_delivery_boys': delivery_boys.count(),
        'active_count': active_deliveries.count(),
    })


@staff_member_required
def delivery_boy_add(request):
    """Create a new user with delivery_boy role and a DeliveryBoy profile."""
    from apps.orders.models import DeliveryBoy

    if request.method == 'POST':
        full_name    = request.POST.get('full_name', '').strip()
        phone        = request.POST.get('phone', '').strip()
        email        = request.POST.get('email', '').strip()
        password     = request.POST.get('password', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        vehicle_num  = request.POST.get('vehicle_number', '').strip()

        if not full_name or not phone or not password:
            messages.error(request, "Name, Phone and Password are required.")
            return redirect('admin_panel:delivery_boy_add')

        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, f"A user with phone {phone} already exists.")
            return redirect('admin_panel:delivery_boy_add')

        user = CustomUser.objects.create_user(
            email=email or f"{phone}@delivery.local",
            phone=phone,
            full_name=full_name,
            password=password,
            role='delivery_boy',
            is_active=True,
        )
        DeliveryBoy.objects.create(
            user=user,
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_num,
            is_available=True,
        )
        messages.success(request, f"Delivery boy '{full_name}' added successfully!")
        return redirect('admin_panel:delivery_manage')

    return render(request, 'admin_panel/delivery_boy_add.html')


@staff_member_required
def delivery_boy_toggle(request, pk):
    """Toggle delivery boy availability."""
    boy_user = get_object_or_404(CustomUser, pk=pk, role='delivery_boy')
    try:
        profile = boy_user.delivery_profile
        profile.is_available = not profile.is_available
        profile.save()
        status = "available" if profile.is_available else "unavailable"
        messages.success(request, f"{boy_user.full_name} marked as {status}.")
    except Exception:
        messages.error(request, "Could not update delivery boy status.")
    return redirect('admin_panel:delivery_manage')


@staff_member_required
def delivery_boy_delete(request, pk):
    """Delete a delivery boy user."""
    boy_user = get_object_or_404(CustomUser, pk=pk, role='delivery_boy')
    if request.method == 'POST':
        name = boy_user.full_name
        boy_user.delete()
        messages.success(request, f"Delivery boy '{name}' deleted.")
        return redirect('admin_panel:delivery_manage')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object': f"Delivery Boy: {boy_user.full_name}",
        'type': 'Delivery Boy',
        'cancel_url': 'admin_panel:delivery_manage',
    })


# ==========================================
# ANALYTICS
# ==========================================

@staff_member_required
def analytics_page(request):
    """Revenue charts, sales trends."""
    from django.db.models import Sum, Count
    from django.db.models.functions import TruncDay, TruncMonth
    from django.utils import timezone
    import json
    
    today = timezone.now()
    
    # Revenue last 30 days
    thirty_days_ago = today - __import__('datetime').timedelta(days=30)
    daily_revenue = (
        Order.objects.filter(
            status='delivered',
            placed_at__gte=thirty_days_ago
        )
        .annotate(day=TruncDay('placed_at'))
        .values('day')
        .annotate(revenue=Sum('total_amount'), orders=Count('id'))
        .order_by('day')
    )
    
    revenue_labels = [str(r['day'].strftime('%d %b')) for r in daily_revenue]
    revenue_data   = [float(r['revenue'] or 0) for r in daily_revenue]
    orders_data    = [r['orders'] for r in daily_revenue]
    
    # Top products
    from apps.products.models import Product
    top_products = Product.objects.filter(is_active=True).order_by('-bought_count')[:10]
    
    # Summary stats
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount'))['total'] or 0
    this_month_revenue = Order.objects.filter(
        status='delivered',
        placed_at__month=today.month,
        placed_at__year=today.year,
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    return render(request, 'admin_panel/analytics_page.html', {
        'revenue_labels': json.dumps(revenue_labels),
        'revenue_data':   json.dumps(revenue_data),
        'orders_data':    json.dumps(orders_data),
        'top_products':   top_products,
        'total_revenue':  total_revenue,
        'this_month_revenue': this_month_revenue,
        'total_orders': Order.objects.count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
    })


# ==========================================
# REPORTS
# ==========================================

@staff_member_required
def reports_page(request):
    """Downloadable Excel/PDF reports."""
    from django.http import HttpResponse
    from django.db.models import Sum, Count
    
    report_type = request.GET.get('type', '')
    date_from   = request.GET.get('from', '')
    date_to     = request.GET.get('to', '')
    
    if report_type == 'orders_csv':
        import csv
        from io import StringIO
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Order #', 'Customer', 'Phone', 'Amount', 'Payment', 'Status', 'Date'])
        
        qs = Order.objects.select_related('user').order_by('-placed_at')
        if date_from:
            qs = qs.filter(placed_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(placed_at__date__lte=date_to)
        
        for order in qs:
            writer.writerow([
                order.order_number,
                order.user.full_name,
                order.user.phone,
                order.total_amount,
                order.payment_method,
                order.status,
                order.placed_at.strftime('%Y-%m-%d %H:%M'),
            ])
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_report.csv"'
        return response
    
    # Summary stats for display
    from django.utils import timezone
    today = timezone.now()
    
    stats = {
        'total_orders': Order.objects.count(),
        'total_revenue': Order.objects.filter(status='delivered').aggregate(
            t=Sum('total_amount'))['t'] or 0,
        'today_orders': Order.objects.filter(placed_at__date=today.date()).count(),
        'today_revenue': Order.objects.filter(
            placed_at__date=today.date(), status='delivered'
        ).aggregate(t=Sum('total_amount'))['t'] or 0,
    }
    
    return render(request, 'admin_panel/reports_page.html', {'stats': stats})


# ==========================================
# STOCK ALERTS
# ==========================================

@staff_member_required
def stock_alerts(request):
    """Low stock warnings."""
    from apps.products.models import Product
    
    low_threshold = int(request.GET.get('threshold', 10))
    
    critical_stock = Product.objects.filter(
        stock__lte=5, is_active=True
    ).select_related('brand', 'category').order_by('stock')
    
    low_stock = Product.objects.filter(
        stock__gt=5, stock__lte=low_threshold, is_active=True
    ).select_related('brand', 'category').order_by('stock')
    
    out_of_stock = Product.objects.filter(
        stock=0, is_active=True
    ).select_related('brand', 'category')
    
    return render(request, 'admin_panel/stock_alerts.html', {
        'critical_stock': critical_stock,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'threshold': low_threshold,
        'critical_count': critical_stock.count(),
        'low_count': low_stock.count(),
        'out_count': out_of_stock.count(),
    })


# ==========================================
# BULK IMPORT
# ==========================================

@staff_member_required
def import_page(request):
    """Excel/CSV bulk product upload."""
    from apps.products.models import Product, Category, Brand
    
    result = None
    if request.method == 'POST' and request.FILES.get('import_file'):
        import_file = request.FILES['import_file']
        file_ext = import_file.name.lower().split('.')[-1]
        
        if file_ext == 'csv':
            import csv, io
            decoded = import_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            created_count = 0
            errors = []
            
            for i, row in enumerate(reader, 1):
                try:
                    name = row.get('name', '').strip()
                    if not name:
                        continue
                    from django.utils.text import slugify
                    price = float(row.get('price', 0) or 0)
                    discount_price = float(row.get('discount_price', price) or price)
                    stock = int(row.get('stock', 0) or 0)
                    
                    # Category / Brand (Auto-create if not found)
                    cat_name   = row.get('category', '').strip()
                    brand_name = row.get('brand', '').strip()

                    category = None
                    if cat_name:
                        category = Category.objects.filter(name__iexact=cat_name).first()
                        if not category:
                            try:
                                category, _ = Category.objects.get_or_create(
                                    name=cat_name,
                                    defaults={'slug': slugify(cat_name)}
                                )
                            except Exception:
                                category = None

                    brand = None
                    if brand_name:
                        brand = Brand.objects.filter(name__iexact=brand_name).first()
                        if not brand:
                            try:
                                brand, _ = Brand.objects.get_or_create(
                                    name=brand_name,
                                    defaults={'slug': slugify(brand_name)}
                                )
                            except Exception:
                                brand = None
                    
                    Product.objects.get_or_create(
                        slug=slugify(name),
                        defaults={
                            'name': name,
                            'price': price,
                            'discount_price': discount_price,
                            'stock': stock,
                            'category': category,
                            'brand': brand,
                            'is_active': True,
                        }
                    )
                    created_count += 1
                except Exception as e:
                    errors.append(f"Row {i}: {e}")
            
            result = {'success': True, 'count': created_count, 'errors': errors}
            messages.success(request, f"Imported {created_count} products successfully.")
        else:
            messages.error(request, "Only CSV files are supported currently.")
    

    return render(request, 'admin_panel/import_page.html', {
        'result': result,
        'total_products': Product.objects.count(),
    })


# ==========================================
# NOTIFICATIONS MANAGEMENT
# ==========================================

@staff_member_required
def notifications_manage(request):
    """Send broadcast or personal notifications, view history."""
    from apps.notifications.models import Notification

    if request.method == 'POST' and request.POST.get('action') == 'send_notification':
        title       = request.POST.get('title', '').strip()
        message     = request.POST.get('message', '').strip()
        notif_type  = request.POST.get('type', 'promo')
        target_type = request.POST.get('target_type', 'all')
        user_id     = request.POST.get('user_id')
        action_url  = request.POST.get('action_url', '').strip()

        if title and message:
            if target_type == 'specific' and user_id:
                try:
                    target_user = CustomUser.objects.get(pk=user_id)
                    Notification.objects.create(
                        user=target_user,
                        title=title,
                        message=message,
                        notif_type=notif_type,
                        action_url=action_url,
                    )
                    messages.success(request, f"Personal notification sent to {target_user.full_name} ({target_user.email})!")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Selected user does not exist.")
            elif target_type == 'delivery':
                boys = CustomUser.objects.filter(role='delivery_boy', is_active=True)
                created = 0
                for boy in boys:
                    Notification.objects.create(
                        user=boy,
                        title=title,
                        message=message,
                        notif_type=notif_type,
                        action_url=action_url,
                    )
                    created += 1
                messages.success(request, f"Notification sent to {created} delivery partners!")
            else:
                # Broadcast to all active users
                customers = CustomUser.objects.filter(role='customer', is_active=True)
                created = 0
                for customer in customers:
                    Notification.objects.create(
                        user=customer,
                        title=title,
                        message=message,
                        notif_type=notif_type,
                        action_url=action_url,
                    )
                    created += 1
                messages.success(request, f"Broadcast notification sent to {created} customers!")
        else:
            messages.error(request, "Title and message are required.")

        return redirect('admin_panel:notifications_manage')

    all_users = CustomUser.objects.filter(is_active=True).order_by('full_name')
    notifications = Notification.objects.select_related('user').order_by('-created_at')[:50]
    return render(request, 'admin_panel/notifications_manage.html', {
        'notifications': notifications,
        'all_users': all_users,
    })


@staff_member_required
def notification_delete(request, pk):
    from apps.notifications.models import Notification
    if request.method == 'POST':
        notif = get_object_or_404(Notification, pk=pk)
        title = notif.title
        notif.delete()
        messages.success(request, f"Notification '{title}' deleted successfully!")
    return redirect('admin_panel:notifications_manage')


@staff_member_required
def pincodes_manage(request):
    from apps.delivery.models import DeliveryPincode
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS delivery_pincodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pincode VARCHAR(10) NOT NULL UNIQUE,
                    area_name VARCHAR(100) NOT NULL DEFAULT '',
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
    except Exception:
        pass

    if request.method == 'POST':
        pincode = request.POST.get('pincode', '').strip()
        area_name = request.POST.get('area_name', '').strip()

        if pincode:
            try:
                obj, created = DeliveryPincode.objects.update_or_create(
                    pincode=pincode,
                    defaults={'area_name': area_name, 'is_active': True}
                )
                action_str = "added" if created else "updated"
                messages.success(request, f"Pincode {pincode} {action_str} successfully!")
            except Exception as e:
                messages.error(request, f"Error saving pincode: {e}")
        else:
            messages.error(request, "Pincode is required.")
        return redirect('admin_panel:pincodes_manage')

    pincodes = list(DeliveryPincode.objects.all().order_by('pincode'))
    active_count = sum(1 for p in pincodes if p.is_active)
    return render(request, 'admin_panel/pincodes_manage.html', {
        'pincodes': pincodes,
        'active_count': active_count,
    })


@staff_member_required
def pincode_toggle(request, pk):
    from apps.delivery.models import DeliveryPincode
    pincode_obj = get_object_or_404(DeliveryPincode, pk=pk)
    pincode_obj.is_active = not pincode_obj.is_active
    pincode_obj.save()
    status_str = "activated" if pincode_obj.is_active else "deactivated"
    messages.success(request, f"Pincode {pincode_obj.pincode} {status_str}.")
    return redirect('admin_panel:pincodes_manage')


@staff_member_required
def pincode_delete(request, pk):
    from apps.delivery.models import DeliveryPincode
    pincode_obj = DeliveryPincode.objects.filter(pk=pk).first()
    if not pincode_obj:
        messages.info(request, "Pincode already deleted or does not exist.")
        return redirect('admin_panel:pincodes_manage')

    code = pincode_obj.pincode
    pincode_obj.delete()
    messages.success(request, f"Pincode {code} deleted successfully.")
    return redirect('admin_panel:pincodes_manage')


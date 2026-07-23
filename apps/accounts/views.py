"""Accounts views — login, register, profile, addresses, logout."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import CustomUser, UserAddress
from apps.orders.models import Order


def login_view(request):
    """Login with email + password."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html')


def register_view(request):
    """Register new customer."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email     = request.POST.get('email', '').strip().lower()
        phone     = request.POST.get('phone', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        password  = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered.')
        else:
            user = CustomUser.objects.create_user(
                email=email, phone=phone, full_name=full_name, password=password
            )
            login(request, user)
            messages.success(request, f'Welcome, {full_name.split()[0]}!')
            return redirect('/')
    
    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    addresses = request.user.addresses.all().order_by('-is_default', '-created_at')
    orders_count = Order.objects.filter(user=request.user).count()
    recent_orders = Order.objects.filter(user=request.user).order_by('-placed_at')[:3]
    
    return render(request, 'accounts/profile.html', {
        'profile_user': request.user,
        'addresses': addresses,
        'orders_count': orders_count,
        'recent_orders': recent_orders,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.full_name = request.POST.get('full_name', user.full_name).strip()
        user.phone     = request.POST.get('phone', user.phone).strip()
        user.email     = request.POST.get('email', user.email).strip().lower()
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile details updated successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html')


@login_required
def address_add(request):
    if request.method == 'POST':
        label        = request.POST.get('label', 'Home')
        full_address = request.POST.get('full_address', '').strip()
        city         = request.POST.get('city', 'Meerut').strip()
        state        = request.POST.get('state', 'Uttar Pradesh').strip()
        pincode      = request.POST.get('pincode', '').strip()
        is_default   = request.POST.get('is_default') == 'on'
        
        if not full_address or not pincode:
            messages.error(request, 'Address and Pincode are required.')
        else:
            addr = UserAddress.objects.create(
                user=request.user,
                label=label,
                full_address=full_address,
                city=city,
                state=state,
                pincode=pincode,
                is_default=is_default
            )
            messages.success(request, 'New delivery address added successfully!')
            return redirect('accounts:profile')
            
    return redirect('accounts:profile')


@login_required
def address_delete(request, pk):
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    addr.delete()
    messages.success(request, 'Address removed successfully.')
    return redirect('accounts:profile')


@login_required
def address_set_default(request, pk):
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    addr.is_default = True
    addr.save()
    messages.success(request, f'Set "{addr.label}" as default address.')
    return redirect('accounts:profile')

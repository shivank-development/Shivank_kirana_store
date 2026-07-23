"""Cart context processor — inject cart into all templates."""


def cart_context(request):
    """Make cart available in every template."""
    cart_count = 0
    cart_total = 0
    
    try:
        if request.user.is_authenticated:
            from apps.cart.models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = cart.item_count
                cart_total = cart.total
        else:
            session_key = request.session.session_key
            if session_key:
                from apps.cart.models import Cart
                cart = Cart.objects.filter(session_key=session_key).first()
                if cart:
                    cart_count = cart.item_count
                    cart_total = cart.total
    except Exception:
        pass
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }

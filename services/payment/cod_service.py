"""
★ COD Service — Shivank Kirana Store
Cash on Delivery with ₹49 advance charge
"""
from utilities.constants import COD_ADVANCE_CHARGE, COD_MIN_ORDER


def calculate_cod_total(order_total: float, delivery_charge: float) -> dict:
    """
    Calculate COD order total with advance charge.
    
    Returns:
        dict: {
            'subtotal': float,
            'delivery': float,
            'cod_advance': int,
            'total': float,
            'pay_now': int,       # ₹49 to pay online upfront
            'pay_on_delivery': float,  # Rest to pay on delivery
        }
    """
    total = order_total + delivery_charge
    pay_on_delivery = total  # Full amount on delivery (advance is separate)
    
    return {
        'subtotal': order_total,
        'delivery': delivery_charge,
        'cod_advance': COD_ADVANCE_CHARGE,
        'total': total,
        'pay_now': COD_ADVANCE_CHARGE,
        'pay_on_delivery': pay_on_delivery,
    }


def is_cod_available(order_total: float, delivery_address: str = "") -> dict:
    """
    Check if COD is available for this order.
    
    Returns:
        dict: {'available': bool, 'reason': str}
    """
    if order_total < COD_MIN_ORDER:
        return {
            'available': False,
            'reason': f'Minimum order ₹{COD_MIN_ORDER} required for COD.'
        }
    
    return {
        'available': True,
        'reason': f'Pay ₹{COD_ADVANCE_CHARGE} advance + rest on delivery.',
        'advance': COD_ADVANCE_CHARGE,
    }


def confirm_cod_by_call(order_id: int, phone: str) -> dict:
    """
    Trigger confirmation call for COD order.
    Returns instructions for the store owner.
    """
    return {
        'action': 'call_required',
        'message': f'Please call {phone} to confirm order #{order_id}',
        'store_phone': '+91 7599342112',
        'order_id': order_id,
    }

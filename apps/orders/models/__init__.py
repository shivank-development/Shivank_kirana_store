# Re-export all models from orders/models.py
# This makes both `models/` folder and `models.py` file coexist correctly.
# Python loads this folder as the `models` module, so we import from models.py
import sys
import importlib
import os

# Import everything from models.py (sibling file)
_models_py = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models.py')

import importlib.util
_spec = importlib.util.spec_from_file_location('apps.orders._models_flat', _models_py)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

# Re-export all public names
Order = _mod.Order
OrderItem = _mod.OrderItem
Payment = _mod.Payment
DeliveryTracking = _mod.DeliveryTracking
DeliveryBoy = _mod.DeliveryBoy
Notification = _mod.Notification
Coupon = _mod.Coupon
StoreSettings = _mod.StoreSettings

__all__ = [
    'Order', 'OrderItem', 'Payment', 'DeliveryTracking',
    'DeliveryBoy', 'Notification', 'Coupon', 'StoreSettings',
]

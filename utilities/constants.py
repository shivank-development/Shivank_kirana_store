"""
★ App-wide Constants — Shivank Kirana Store
Single source of truth for all business constants
"""

# ── STORE INFO ──
STORE_NAME = "Shivank Kirana Store"
STORE_PHONE = "+91 7599342112"
STORE_WHATSAPP = "+917599342112"
STORE_EMAIL = "shivankirana@gmail.com"
STORE_ADDRESS = "288, Main Market, Meerut, UP"
STORE_LAT = 28.9845
STORE_LNG = 77.7064

# ── PAYMENT ──
UPI_ID = "7060169850@ptyes"
UPI_NAME = "Shivank Kirana Store"
COD_ADVANCE_CHARGE = 49            # ₹49 advance for COD orders
COD_MIN_ORDER = 100                # Minimum order for COD

# ── DELIVERY ──
FREE_DELIVERY_ABOVE = 799          # ₹799+ → free delivery
DELIVERY_CHARGE = 49               # Standard delivery charge
FREE_DELIVERY_KM = 5               # Free zone radius in km
PER_KM_RATE = 10                   # ₹10/km beyond free zone
MAX_DELIVERY_KM = 20               # Maximum delivery distance

# ── ORDER ──
ORDER_NUMBER_PREFIX = "ORD"
ORDER_NUMBER_FORMAT = "ORD-{year}-{seq:05d}"   # e.g. ORD-2026-00001

# ── PAGINATION ──
PRODUCTS_PER_PAGE = 24
ORDERS_PER_PAGE = 10
ADMIN_ITEMS_PER_PAGE = 25

# ── STOCK ──
LOW_STOCK_THRESHOLD = 10           # Alert when stock ≤ 10 units
OUT_OF_STOCK_THRESHOLD = 0

# ── DISCOUNTS ──
MAX_COUPON_DISCOUNT_PERCENT = 50   # Max 50% off via coupon

# ── USER ROLES ──
ROLE_CUSTOMER = 'customer'
ROLE_ADMIN = 'admin'
ROLE_DELIVERY = 'delivery'

# ── ORDER STATUSES ──
ORDER_STATUS_PENDING = 'pending'
ORDER_STATUS_CONFIRMED = 'confirmed'
ORDER_STATUS_PREPARING = 'preparing'
ORDER_STATUS_DISPATCHED = 'dispatched'
ORDER_STATUS_DELIVERED = 'delivered'
ORDER_STATUS_CANCELLED = 'cancelled'

ORDER_STATUSES = [
    (ORDER_STATUS_PENDING, 'Pending'),
    (ORDER_STATUS_CONFIRMED, 'Confirmed'),
    (ORDER_STATUS_PREPARING, 'Preparing'),
    (ORDER_STATUS_DISPATCHED, 'Dispatched'),
    (ORDER_STATUS_DELIVERED, 'Delivered'),
    (ORDER_STATUS_CANCELLED, 'Cancelled'),
]

# ── PAYMENT STATUSES ──
PAYMENT_PENDING = 'pending'
PAYMENT_SUCCESS = 'success'
PAYMENT_FAILED = 'failed'
PAYMENT_REFUNDED = 'refunded'

# ── NOTIFICATION TYPES ──
NOTIF_ORDER_PLACED = 'order_placed'
NOTIF_ORDER_CONFIRMED = 'order_confirmed'
NOTIF_OUT_FOR_DELIVERY = 'out_for_delivery'
NOTIF_DELIVERED = 'delivered'
NOTIF_LOW_STOCK = 'low_stock'

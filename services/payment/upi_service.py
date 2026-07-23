"""
★ UPI Payment Service — Shivank Kirana Store
UPI ID: 7060169850@ptyes
"""
import qrcode
import io
import base64
from urllib.parse import quote

UPI_ID = "7060169850@ptyes"
UPI_NAME = "Shivank Kirana Store"


def generate_upi_payment_url(amount: float, order_number: str, note: str = "") -> str:
    """
    Generate UPI deep link URL for payment.
    Format: upi://pay?pa=UPI_ID&pn=NAME&am=AMOUNT&tn=NOTE
    """
    note = note or f"Order {order_number}"
    url = (
        f"upi://pay?"
        f"pa={quote(UPI_ID)}"
        f"&pn={quote(UPI_NAME)}"
        f"&am={amount:.2f}"
        f"&tn={quote(note)}"
        f"&cu=INR"
    )
    return url


def generate_upi_qr_base64(amount: float, order_number: str) -> str:
    """
    Generate QR code as base64 string for embedding in HTML.
    Returns: data:image/png;base64,<base64_string>
    """
    upi_url = generate_upi_payment_url(amount, order_number)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#1a5d1a", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{b64}"


def verify_upi_payment(txn_id: str, expected_amount: float) -> dict:
    """
    Verify UPI payment transaction.
    NOTE: Manual verification — admin marks as paid after checking screenshot.
    
    Returns:
        dict: {'verified': bool, 'message': str}
    """
    # In production: integrate with payment gateway API
    # For now: return pending — admin verifies manually
    return {
        'verified': False,
        'status': 'pending_verification',
        'message': 'Payment verification pending. Admin will confirm within 2-5 minutes.',
        'txn_id': txn_id,
    }

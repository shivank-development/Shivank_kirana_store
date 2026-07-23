"""
Helper Functions — Shivank Kirana Store
"""
from django.utils.text import slugify as django_slugify
import re


def slugify(text: str) -> str:
    """Create URL-safe slug from text."""
    return django_slugify(text)


def format_price(amount: float) -> str:
    """Format price as Indian Rupee string."""
    return f"₹{amount:,.0f}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_length characters."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_phone(phone: str) -> str:
    """Clean and normalize Indian phone number."""
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('91') and len(digits) == 12:
        digits = digits[2:]
    if len(digits) == 10:
        return f"+91{digits}"
    return phone


def calculate_discount_percent(original: float, selling: float) -> int:
    """Calculate discount percentage."""
    if original <= 0 or selling >= original:
        return 0
    return round(((original - selling) / original) * 100)


def get_star_range(rating: float):
    """Return star display data for a rating value (0-5)."""
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return {
        'full': full_stars,
        'half': half_star,
        'empty': empty_stars,
        'rating': rating,
    }


def paginate_list(items: list, page: int = 1, per_page: int = 24) -> tuple:
    """Simple list paginator. Returns (page_items, total_count)."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total

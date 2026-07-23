"""Create stub templates for Shivank Kirana Store."""
import os

templates = {}

templates['templates/errors/404.html'] = """{% extends 'base/base.html' %}
{% block title %}404 Not Found{% endblock %}
{% block content %}
<div style="text-align:center; padding: 80px 20px;">
  <div style="font-size: 6rem;">🔍</div>
  <h1 style="font-size: 3rem; color: var(--clr-primary-dark);">404</h1>
  <p style="font-size: 1.2rem; color: #666;">Page not found!</p>
  <a href="/" class="btn btn-primary" style="margin-top: 20px;">Go Home</a>
</div>
{% endblock %}
"""

templates['templates/errors/500.html'] = """{% extends 'base/base.html' %}
{% block title %}500 Server Error{% endblock %}
{% block content %}
<div style="text-align:center; padding: 80px 20px;">
  <div style="font-size: 6rem;">⚠️</div>
  <h1 style="font-size: 3rem; color: red;">500</h1>
  <p>Something went wrong. Please try again later.</p>
  <a href="/" class="btn btn-primary" style="margin-top: 20px;">Go Home</a>
</div>
{% endblock %}
"""

templates['templates/wishlist/wishlist_list.html'] = """{% extends 'base/base.html' %}
{% block title %}My Wishlist{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">My Wishlist</h1>
  {% if items %}
    <div class="grid-4">
      {% for item in items %}
        {% include 'products/product_card.html' with product=item.product %}
      {% endfor %}
    </div>
  {% else %}
    <div style="text-align:center; padding:60px;">
      <div style="font-size:4rem">❤️</div>
      <p>Your wishlist is empty. Start adding products!</p>
      <a href="/shop/" class="btn btn-primary" style="margin-top:20px">Browse Products</a>
    </div>
  {% endif %}
</div>
{% endblock %}
"""

templates['templates/orders/order_list.html'] = """{% extends 'base/base.html' %}
{% block title %}My Orders{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">My Orders</h1>
  {% if orders %}
    {% for order in orders %}
    <div class="card p-lg mb-md">
      <div class="flex-between">
        <strong>{{ order.order_number }}</strong>
        <span class="price-main">Rs {{ order.total_amount }}</span>
      </div>
      <div style="font-size:0.875rem; color:#888;">{{ order.placed_at|date:"d M Y" }}</div>
      <a href="/orders/{{ order.id }}/" class="btn btn-outline-primary btn-sm mt-sm">View Details</a>
    </div>
    {% endfor %}
  {% else %}
    <div style="text-align:center; padding:60px;">
      <div style="font-size:4rem">📦</div>
      <p>No orders yet.</p>
      <a href="/shop/" class="btn btn-primary" style="margin-top:20px">Shop Now</a>
    </div>
  {% endif %}
</div>
{% endblock %}
"""

templates['templates/orders/order_detail.html'] = """{% extends 'base/base.html' %}
{% block title %}Order {{ order.order_number }}{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Order {{ order.order_number }}</h1>
  <div class="card p-lg">
    <p><strong>Status:</strong> {{ order.get_status_display }}</p>
    <p><strong>Total:</strong> Rs {{ order.total_amount }}</p>
    <p><strong>Payment:</strong> {{ order.payment_method }}</p>
    <p><strong>Placed:</strong> {{ order.placed_at|date:"d M Y, g:i A" }}</p>
  </div>
</div>
{% endblock %}
"""

templates['templates/cart/cart.html'] = """{% extends 'base/base.html' %}
{% block title %}My Cart{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">My Cart</h1>
  {% if items %}
    {% for item in items %}
    <div class="card p-lg mb-md" data-cart-item="{{ item.id }}">
      <div class="flex-between">
        <strong>{{ item.product.name }}</strong>
        <span>Qty: {{ item.quantity }}</span>
        <span class="price-main">Rs {{ item.product.selling_price }}</span>
      </div>
    </div>
    {% endfor %}
    <div class="card p-lg mt-md">
      <div class="flex-between">
        <span>Total</span>
        <span class="price-main">Rs {{ cart.total }}</span>
      </div>
      <a href="/checkout/" class="btn btn-primary btn-full mt-md">Proceed to Checkout</a>
    </div>
  {% else %}
    <div style="text-align:center; padding:60px;">
      <div style="font-size:4rem">🛒</div>
      <p>Your cart is empty!</p>
      <a href="/shop/" class="btn btn-primary" style="margin-top:20px">Shop Now</a>
    </div>
  {% endif %}
</div>
{% endblock %}
"""

templates['templates/accounts/profile.html'] = """{% extends 'base/base.html' %}
{% block title %}My Profile{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">My Profile</h1>
  <div class="card p-lg" style="max-width:500px;">
    <p><strong>Name:</strong> {{ profile_user.full_name }}</p>
    <p><strong>Email:</strong> {{ profile_user.email }}</p>
    <p><strong>Phone:</strong> {{ profile_user.phone }}</p>
    <a href="/auth/profile/edit/" class="btn btn-primary btn-sm mt-md">Edit Profile</a>
  </div>
</div>
{% endblock %}
"""

templates['templates/accounts/edit_profile.html'] = """{% extends 'base/base.html' %}
{% block title %}Edit Profile{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Edit Profile</h1>
  <div class="card p-lg" style="max-width:500px;">
    <form method="POST">
      {% csrf_token %}
      <div style="margin-bottom:16px;">
        <label style="font-weight:600;display:block;margin-bottom:6px;">Full Name</label>
        <input type="text" name="full_name" value="{{ request.user.full_name }}"
               style="width:100%;padding:12px;border:2px solid #eee;border-radius:10px;">
      </div>
      <div style="margin-bottom:16px;">
        <label style="font-weight:600;display:block;margin-bottom:6px;">Email</label>
        <input type="email" name="email" value="{{ request.user.email }}"
               style="width:100%;padding:12px;border:2px solid #eee;border-radius:10px;">
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </form>
  </div>
</div>
{% endblock %}
"""

templates['templates/search/search_results.html'] = """{% extends 'base/base.html' %}
{% block title %}Search: {{ query }}{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Search: "{{ query }}"</h1>
  {% if products %}
    <div class="grid-4">
      {% for product in products %}
        {% include 'products/product_card.html' with product=product %}
      {% endfor %}
    </div>
  {% else %}
    <div style="text-align:center;padding:60px;">
      <div style="font-size:4rem">🔍</div>
      <p>No products found for "{{ query }}"</p>
      <a href="/shop/" class="btn btn-primary" style="margin-top:20px">Browse All</a>
    </div>
  {% endif %}
</div>
{% endblock %}
"""

templates['templates/checkout/checkout.html'] = """{% extends 'base/base.html' %}
{% block title %}Checkout{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Checkout</h1>
  <div class="card p-lg" style="max-width:600px;">
    <p>Please complete your order via WhatsApp for instant confirmation.</p>
    <a href="https://wa.me/917599342112?text=Hi!%20I%20want%20to%20place%20an%20order"
       class="btn btn-whatsapp btn-lg" style="margin-top:16px;" target="_blank">
      Order on WhatsApp
    </a>
  </div>
</div>
{% endblock %}
"""

templates['templates/admin_panel/dashboard.html'] = """{% extends 'base/base.html' %}
{% block title %}Admin Dashboard{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Admin Dashboard</h1>
  <div class="grid-4 mb-lg">
    <div class="card p-lg text-center">
      <div style="font-size:2rem;font-weight:800;color:var(--clr-primary)">{{ total_orders }}</div>
      <p>Total Orders</p>
    </div>
    <div class="card p-lg text-center">
      <div style="font-size:2rem;font-weight:800;color:var(--clr-primary)">{{ total_products }}</div>
      <p>Products</p>
    </div>
    <div class="card p-lg text-center">
      <div style="font-size:2rem;font-weight:800;color:var(--clr-primary)">{{ total_users }}</div>
      <p>Customers</p>
    </div>
    <div class="card p-lg text-center">
      <div style="font-size:2rem;font-weight:800;">{{ pending_orders }}</div>
      <p>Pending Orders</p>
    </div>
  </div>
  <a href="/django-admin/" class="btn btn-primary">Go to Django Admin</a>
</div>
{% endblock %}
"""

templates['templates/delivery/delivery.html'] = """{% extends 'base/base.html' %}
{% block title %}Delivery{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Delivery Tracking</h1>
  <p>Track your orders in real-time. Feature coming soon!</p>
</div>
{% endblock %}
"""

templates['templates/notifications/notifications.html'] = """{% extends 'base/base.html' %}
{% block title %}Notifications{% endblock %}
{% block content %}
<div class="container section">
  <h1 class="section-title">Notifications</h1>
  <p>No new notifications.</p>
</div>
{% endblock %}
"""

templates['templates/products/product_list.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}{% if page_title %}{{ page_title }}{% else %}Shop All Products{% endif %} — Shivank Kirana Store{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    <h1 class="section-title">
      {% if category %}{{ category.name }}
      {% elif brand %}{{ brand.name }}
      {% elif search_query %}Search: "{{ search_query }}"
      {% else %}All Products{% endif %}
    </h1>
    {% if products %}
      <div class="grid-4">
        {% for product in products %}
          {% include 'products/product_card.html' with product=product %}
        {% endfor %}
      </div>
      {% if page_obj %}
        <div style="text-align:center; margin-top:32px;">
          {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline-primary btn-sm">← Prev</a>
          {% endif %}
          <span style="margin: 0 16px; color: #666;">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
          {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline-primary btn-sm">Next →</a>
          {% endif %}
        </div>
      {% endif %}
    {% else %}
      <div style="text-align:center; padding:60px;">
        <div style="font-size:4rem">📦</div>
        <p>No products found.</p>
        <a href="/shop/" class="btn btn-primary" style="margin-top:20px">Browse All</a>
      </div>
    {% endif %}
  </div>
</section>
{% endblock %}
"""

templates['templates/products/product_detail.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}{{ product.name }} — Shivank Kirana Store{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:48px; align-items:start;">
      <div class="card" style="padding:32px; text-align:center;">
        {% if product.image_main %}
          <img src="{{ product.image_main.url }}" alt="{{ product.name }}" style="max-height:350px; object-fit:contain; width:100%;">
        {% else %}
          <div style="height:350px; background:var(--clr-light-grey); border-radius:16px; display:flex; align-items:center; justify-content:center;">
            <i class="fa-solid fa-image" style="font-size:4rem; color:#ccc;"></i>
          </div>
        {% endif %}
      </div>
      <div>
        {% if product.brand %}<a href="/brand/{{ product.brand.slug }}/" style="color:var(--clr-primary);font-weight:600;">{{ product.brand.name }}</a>{% endif %}
        <h1 style="font-size:1.8rem; font-weight:800; margin:8px 0;">{{ product.name }}</h1>
        {% if product.weight %}<span class="product-weight">{{ product.weight }}</span>{% endif %}
        <div class="product-price-row" style="margin:16px 0;">
          <span class="price-main" style="font-size:2rem;">Rs {{ product.selling_price }}</span>
          {% if product.discount_price %}<span class="price-mrp">Rs {{ product.price }}</span>{% endif %}
          {% if product.discount_percent > 0 %}<span class="badge badge-discount">{{ product.discount_percent }}% OFF</span>{% endif %}
        </div>
        {% if product.description %}<p style="color:#666; line-height:1.7;">{{ product.description }}</p>{% endif %}
        <div style="margin-top:24px; display:flex; gap:12px; align-items:center;">
          <div class="qty-selector">
            <button class="qty-btn" onclick="changeQty(this, -1)">-</button>
            <input type="number" class="qty-input" data-qty value="1" min="1" max="{{ product.stock }}">
            <button class="qty-btn" onclick="changeQty(this, 1)">+</button>
          </div>
          {% if product.in_stock %}
            <button class="btn btn-primary" data-add-to-cart="{{ product.id }}" style="flex:1;">
              Add to Cart
            </button>
          {% else %}
            <button class="btn" disabled style="background:var(--clr-text-muted);color:white;flex:1;">Out of Stock</button>
          {% endif %}
        </div>
        <div class="product-delivery" style="margin-top:12px;">
          <i class="fa-solid fa-truck-fast"></i>
          <span>{{ product.delivery_eta }}</span>
        </div>
      </div>
    </div>
    {% if related %}
      <div class="section-header" style="margin-top:48px;">
        <h2 class="section-title">Related Products</h2>
      </div>
      <div class="grid-4">
        {% for p in related %}
          {% include 'products/product_card.html' with product=p %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
</section>
{% endblock %}
"""

created = 0
for path, content in templates.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        created += 1
        print(f'Created: {path}')
    else:
        print(f'Exists:  {path}')

print(f'\nDone: {created} new templates created')

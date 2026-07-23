"""
Build all remaining key templates and copy brand/category assets.
Run: python scripts/build_pages.py
"""
import os, shutil, re

# ─── 1. Read SVG icons from Category_icon HTML files ───────────────────────
def extract_svg(html_content):
    start = html_content.find('<svg')
    end   = html_content.find('</svg>') + 6
    if start == -1:
        return ''
    svg = html_content[start:end]
    # Normalise class attribute so it works inline
    svg = re.sub(r'class="[^"]*"', 'width="32" height="32"', svg)
    return svg

icon_dir = 'shop_images/Category_icon'
cat_icons = {}
for fname in os.listdir(icon_dir):
    path = os.path.join(icon_dir, fname)
    with open(path, encoding='utf-8') as f:
        cat_icons[fname.replace('.html','').strip()] = extract_svg(f.read())

print(f"Loaded {len(cat_icons)} category icons")

# ─── 2. Copy brand logos to static/images/brands/ ──────────────────────────
brand_logo_src = 'shop_images/Company_Brand_logo'
brand_logo_dst = 'static/images/brands'
os.makedirs(brand_logo_dst, exist_ok=True)

copied_logos = {}
if os.path.exists(brand_logo_src):
    for fname in os.listdir(brand_logo_src):
        src = os.path.join(brand_logo_src, fname)
        dst = os.path.join(brand_logo_dst, fname)
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
        if os.path.isfile(src):
            copied_logos[fname] = f'/static/images/brands/{fname}'
    print(f"Brand logos available: {len(copied_logos)}")
else:
    print("No brand logo directory found — skipping")

# ─── 3. Build templates ─────────────────────────────────────────────────────
TEMPLATES = {}

# ── brand_page.html ──
TEMPLATES['templates/brands/brand_page.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}{{ brand.name }} Products — Shivank Kirana Store{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    <!-- Brand Header -->
    <div class="brand-hero">
      {% if brand.logo %}
        <img src="{{ brand.logo.url }}" alt="{{ brand.name }}" class="brand-hero-logo">
      {% endif %}
      <div class="brand-hero-info">
        <h1 class="brand-hero-name">{{ brand.name }}</h1>
        {% if brand.description %}<p class="brand-hero-desc">{{ brand.description }}</p>{% endif %}
        <span class="brand-product-count">{{ products.count }} products available</span>
      </div>
    </div>

    {% if products %}
      <div class="grid-4 mt-xl">
        {% for product in products %}
          {% include 'products/product_card.html' with product=product %}
        {% endfor %}
      </div>
    {% else %}
      <div class="empty-state">
        <div style="font-size:4rem">📦</div>
        <h3>No products yet for {{ brand.name }}</h3>
        <a href="/shop/" class="btn btn-primary mt-md">Browse All Products</a>
      </div>
    {% endif %}
  </div>
</section>
{% endblock %}
"""

# ── category_page.html ──
TEMPLATES['templates/categories/category_page.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}{{ category.name }} — Shivank Kirana Store{% endblock %}
{% block content %}
<section class="section">
  <div class="container">
    <!-- Category Header -->
    <div class="cat-page-header">
      <h1 class="section-title">{{ category.name }}</h1>
      {% if category.description %}
        <p style="color:var(--clr-text-medium); margin-top:8px;">{{ category.description }}</p>
      {% endif %}
      <div class="cat-breadcrumb">
        <a href="/">Home</a> <span>/</span>
        <a href="/shop/">Products</a> <span>/</span>
        <span class="active">{{ category.name }}</span>
      </div>
    </div>

    {% if products %}
      <div class="grid-4">
        {% for product in products %}
          {% include 'products/product_card.html' with product=product %}
        {% endfor %}
      </div>
    {% else %}
      <div class="empty-state">
        <div style="font-size:4rem">🛒</div>
        <h3>No products in {{ category.name }} yet</h3>
        <a href="/shop/" class="btn btn-primary mt-md">Browse All Products</a>
      </div>
    {% endif %}
  </div>
</section>
{% endblock %}
"""

# ── order_success.html ──
TEMPLATES['templates/orders/order_success.html'] = """{% extends 'base/base.html' %}
{% block title %}Order Placed Successfully!{% endblock %}
{% block content %}
<div class="container section" style="text-align:center; max-width:560px; margin:0 auto;">
  <div class="success-card anim-fadeInUp">
    <div class="success-icon">✅</div>
    <h1 style="font-size:2rem; font-weight:800; color:var(--clr-primary-dark); margin:16px 0 8px;">
      Order Placed!
    </h1>
    <p style="color:var(--clr-text-medium); font-size:1.05rem;">
      Your order <strong>{{ order.order_number }}</strong> has been placed successfully.
    </p>
    <div class="order-details-box">
      <div class="detail-row">
        <span>Total Amount</span>
        <strong>₹{{ order.total_amount }}</strong>
      </div>
      <div class="detail-row">
        <span>Payment Method</span>
        <strong>{{ order.payment_method|upper }}</strong>
      </div>
      <div class="detail-row">
        <span>Estimated Delivery</span>
        <strong>30–60 minutes</strong>
      </div>
    </div>
    <div style="margin-top:24px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
      <a href="/orders/{{ order.id }}/" class="btn btn-primary">Track Order</a>
      <a href="/shop/" class="btn btn-outline-primary">Continue Shopping</a>
      <a href="https://wa.me/917599342112?text=Hi!%20My%20order%20{{ order.order_number }}%20is%20placed." 
         class="btn btn-whatsapp" target="_blank">WhatsApp Update</a>
    </div>
  </div>
</div>
<style>
.success-card { background:white; border-radius:24px; padding:48px 32px; box-shadow:var(--shadow-float); }
.success-icon { font-size:5rem; line-height:1; animation: bounceIn 0.6s ease; }
@keyframes bounceIn { 0%{transform:scale(0)} 70%{transform:scale(1.1)} 100%{transform:scale(1)} }
.order-details-box { background:var(--clr-mint-bg,#e8f5e9); border-radius:16px; padding:20px 24px; margin:24px 0; text-align:left; }
.detail-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(0,0,0,0.06); font-size:0.95rem; }
.detail-row:last-child { border-bottom:none; }
</style>
{% endblock %}
"""

# ── checkout.html (full) ──
TEMPLATES['templates/checkout/checkout.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}Checkout — Shivank Kirana Store{% endblock %}
{% block extra_css %}
<style>
.checkout-grid { display:grid; grid-template-columns:1fr 380px; gap:32px; }
.checkout-section { background:white; border-radius:20px; box-shadow:var(--shadow-card); padding:28px; margin-bottom:24px; }
.checkout-section-title { font-family:var(--font-heading); font-size:1.1rem; font-weight:700; color:var(--clr-primary-dark); margin-bottom:20px; display:flex; align-items:center; gap:8px; }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.form-group { margin-bottom:16px; }
.form-group label { display:block; font-weight:600; font-size:0.85rem; color:var(--clr-text-dark); margin-bottom:6px; }
.form-control { width:100%; padding:12px 14px; border:2px solid var(--clr-border); border-radius:10px; font-size:0.95rem; outline:none; transition:border-color 0.2s; }
.form-control:focus { border-color:var(--clr-primary); }
.payment-option { border:2px solid var(--clr-border); border-radius:14px; padding:16px 20px; margin-bottom:12px; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:12px; }
.payment-option:has(input:checked), .payment-option.selected { border-color:var(--clr-primary); background:var(--clr-mint-bg,#e8f5e9); }
.payment-option input[type=radio] { accent-color:var(--clr-primary); width:18px; height:18px; }
.payment-icon { font-size:1.5rem; }
.payment-label strong { display:block; font-size:0.95rem; }
.payment-label small { color:var(--clr-text-medium); font-size:0.8rem; }
.order-summary-item { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--clr-border); font-size:0.9rem; }
.order-summary-item:last-child { border-bottom:none; }
.summary-total { display:flex; justify-content:space-between; padding:16px 0 0; font-size:1.1rem; font-weight:800; color:var(--clr-primary-dark); }
.upi-section, .cod-section { display:none; margin-top:16px; padding:16px; background:#f8f9fa; border-radius:12px; text-align:center; }
.upi-section.active, .cod-section.active { display:block; }
.upi-qr { width:180px; height:180px; border-radius:12px; border:3px solid var(--clr-primary); padding:8px; background:white; margin:0 auto 12px; display:block; }
@media(max-width:900px) { .checkout-grid { grid-template-columns:1fr; } }
</style>
{% endblock %}

{% block content %}
<div class="container section">
  <h1 class="section-title" style="margin-bottom:28px;">🛒 Checkout</h1>
  
  <form method="POST" action="/checkout/place-order/" id="checkout-form">
    {% csrf_token %}
    <div class="checkout-grid">
      <!-- LEFT: Address + Payment -->
      <div>
        <!-- Delivery Address -->
        <div class="checkout-section">
          <h2 class="checkout-section-title">📍 Delivery Address</h2>
          <div class="form-row">
            <div class="form-group">
              <label>Full Name *</label>
              <input type="text" name="full_name" class="form-control" 
                     value="{% if request.user.is_authenticated %}{{ request.user.full_name }}{% endif %}" required>
            </div>
            <div class="form-group">
              <label>Mobile Number *</label>
              <input type="tel" name="phone" class="form-control"
                     value="{% if request.user.is_authenticated %}{{ request.user.phone }}{% endif %}" required>
            </div>
          </div>
          <div class="form-group">
            <label>Full Address *</label>
            <textarea name="address" class="form-control" rows="3" placeholder="House No., Street, Landmark..." required></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>City</label>
              <input type="text" name="city" class="form-control" value="Meerut">
            </div>
            <div class="form-group">
              <label>Pincode *</label>
              <input type="text" name="pincode" class="form-control" placeholder="250404" maxlength="6" required>
            </div>
          </div>
          <div class="form-group">
            <label>Delivery Instructions (Optional)</label>
            <input type="text" name="instructions" class="form-control" placeholder="Ring bell, leave at gate...">
          </div>
        </div>

        <!-- Payment Method -->
        <div class="checkout-section">
          <h2 class="checkout-section-title">💳 Payment Method</h2>
          
          <label class="payment-option" id="upi-opt">
            <input type="radio" name="payment_method" value="upi" checked>
            <span class="payment-icon">📱</span>
            <div class="payment-label">
              <strong>UPI / QR Code</strong>
              <small>Pay via Paytm, PhonePe, Google Pay, BHIM</small>
            </div>
          </label>
          
          <label class="payment-option" id="cod-opt">
            <input type="radio" name="payment_method" value="cod">
            <span class="payment-icon">💵</span>
            <div class="payment-label">
              <strong>Cash on Delivery (COD)</strong>
              <small>₹49 advance required · Rest on delivery</small>
            </div>
          </label>

          <!-- UPI Section -->
          <div class="upi-section active" id="upi-details">
            <p style="font-weight:600; margin-bottom:12px;">Scan QR Code to Pay</p>
            <img src="/static/images/payment/Qr_code_image.jpeg" alt="UPI QR" class="upi-qr"
                 onerror="this.style.display='none'">
            <p style="font-size:0.85rem; color:#666;">UPI ID: <strong>7060169850@ptyes</strong></p>
            <p style="font-size:0.8rem; color:#888; margin-top:4px;">After payment, enter UTR / Transaction ID:</p>
            <div class="form-group" style="margin-top:8px; text-align:left;">
              <input type="text" name="utr_number" id="utr-input" class="form-control" 
                     placeholder="e.g. 123456789012">
            </div>
          </div>

          <!-- COD Section -->
          <div class="cod-section" id="cod-details">
            <div style="background:#fff3cd; border:1px solid #ffc107; border-radius:10px; padding:16px; text-align:left;">
              <p style="font-weight:700; color:#856404;">⚠️ COD Terms</p>
              <ul style="font-size:0.85rem; color:#856404; margin:8px 0 0 16px; line-height:1.8;">
                <li>Pay <strong>₹49 advance via UPI</strong> to confirm order</li>
                <li>Rest of amount paid on delivery</li>
                <li>UPI ID: <strong>7060169850@ptyes</strong></li>
              </ul>
            </div>
            <div class="form-group" style="margin-top:12px; text-align:left;">
              <label>Advance Payment UTR *</label>
              <input type="text" name="cod_advance_utr" class="form-control" 
                     placeholder="₹49 advance UTR number">
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Order Summary -->
      <div>
        <div class="checkout-section" style="position:sticky; top:100px;">
          <h2 class="checkout-section-title">🧾 Order Summary</h2>
          {% for item in cart_items %}
          <div class="order-summary-item">
            <span>{{ item.product.name }} × {{ item.quantity }}</span>
            <span>₹{{ item.subtotal }}</span>
          </div>
          {% endfor %}
          <div class="order-summary-item">
            <span>Subtotal</span>
            <span>₹{{ subtotal }}</span>
          </div>
          <div class="order-summary-item">
            <span>Delivery Charge</span>
            <span>{% if delivery_charge == 0 %}<span style="color:var(--clr-primary)">FREE</span>{% else %}₹{{ delivery_charge }}{% endif %}</span>
          </div>
          <div class="summary-total">
            <span>Total</span>
            <span>₹{{ total }}</span>
          </div>
          <button type="submit" class="btn btn-primary btn-full" style="margin-top:20px; padding:16px; font-size:1rem;">
            <i class="fa-solid fa-bag-shopping"></i>
            Place Order
          </button>
          <a href="https://wa.me/917599342112?text=Hi!%20I%20want%20to%20place%20an%20order"
             class="btn btn-whatsapp btn-full" style="margin-top:10px;" target="_blank">
            Order via WhatsApp Instead
          </a>
        </div>
      </div>
    </div>
  </form>
</div>

<script>
document.querySelectorAll('input[name=payment_method]').forEach(radio => {
  radio.addEventListener('change', () => {
    document.getElementById('upi-details').classList.toggle('active', radio.value === 'upi' && radio.checked);
    document.getElementById('cod-details').classList.toggle('active', radio.value === 'cod' && radio.checked);
    document.getElementById('utr-input').required = (radio.value === 'upi');
  });
});
document.querySelectorAll('.payment-option').forEach(opt => {
  opt.addEventListener('click', () => {
    document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
    opt.classList.add('selected');
  });
});
</script>
{% endblock %}
"""

# ── Proper cart page ──
TEMPLATES['templates/cart/cart.html'] = """{% extends 'base/base.html' %}
{% load static %}
{% block title %}My Cart — Shivank Kirana Store{% endblock %}
{% block extra_css %}
<style>
.cart-layout { display:grid; grid-template-columns:1fr 360px; gap:28px; align-items:start; }
.cart-item-card { display:flex; align-items:center; gap:16px; background:white; border-radius:16px; padding:20px; box-shadow:var(--shadow-card); margin-bottom:16px; }
.cart-item-img { width:80px; height:80px; object-fit:contain; border-radius:10px; flex-shrink:0; background:#f8f8f8; }
.cart-item-info { flex:1; }
.cart-item-name { font-weight:700; color:var(--clr-text-dark); margin-bottom:4px; }
.cart-item-weight { font-size:0.8rem; color:var(--clr-text-medium); }
.cart-item-price { font-size:1.1rem; font-weight:800; color:var(--clr-primary-dark); }
.cart-qty-control { display:flex; align-items:center; gap:8px; }
.qty-btn { width:30px; height:30px; border-radius:50%; border:2px solid var(--clr-primary); color:var(--clr-primary); background:white; font-size:1rem; font-weight:700; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; justify-content:center; }
.qty-btn:hover { background:var(--clr-primary); color:white; }
.qty-val { font-weight:700; font-size:1rem; min-width:24px; text-align:center; }
.remove-btn { color:var(--clr-danger,#dc3545); border:none; background:none; font-size:0.8rem; cursor:pointer; margin-top:8px; }
.summary-card { background:white; border-radius:20px; box-shadow:var(--shadow-card); padding:24px; position:sticky; top:100px; }
.summary-row { display:flex; justify-content:space-between; padding:10px 0; font-size:0.9rem; border-bottom:1px solid var(--clr-border); }
.summary-row:last-of-type { border-bottom:none; }
.summary-total { display:flex; justify-content:space-between; font-size:1.15rem; font-weight:800; padding:16px 0 0; color:var(--clr-primary-dark); }
.free-del-banner { background:var(--clr-mint-bg,#e8f5e9); border:1px solid var(--clr-primary); border-radius:10px; padding:10px 16px; font-size:0.85rem; color:var(--clr-primary-dark); margin-bottom:16px; }
@media(max-width:900px) { .cart-layout { grid-template-columns:1fr; } }
</style>
{% endblock %}

{% block content %}
<div class="container section">
  <h1 class="section-title" style="margin-bottom:24px;">🛒 My Cart
    <span style="font-size:1rem; font-weight:400; color:var(--clr-text-medium);">
      ({{ cart_count }} item{{ cart_count|pluralize }})
    </span>
  </h1>

  {% if items %}
  <div class="cart-layout">
    <!-- Cart Items -->
    <div>
      {% for item in items %}
      <div class="cart-item-card" id="cart-item-{{ item.id }}">
        {% if item.product.image_main %}
          <img src="{{ item.product.image_main.url }}" alt="{{ item.product.name }}" class="cart-item-img">
        {% else %}
          <div class="cart-item-img" style="display:flex;align-items:center;justify-content:center;font-size:2rem;">🛍️</div>
        {% endif %}
        <div class="cart-item-info">
          <p class="cart-item-name">{{ item.product.name }}</p>
          {% if item.product.weight %}<p class="cart-item-weight">{{ item.product.weight }}</p>{% endif %}
          <p class="cart-item-price">₹{{ item.product.selling_price }}</p>
          <div class="cart-qty-control">
            <button class="qty-btn" onclick="updateCartQty({{ item.id }}, {{ item.quantity|add:'-1' }})">−</button>
            <span class="qty-val">{{ item.quantity }}</span>
            <button class="qty-btn" onclick="updateCartQty({{ item.id }}, {{ item.quantity|add:'1' }})">+</button>
          </div>
          <button class="remove-btn" onclick="removeFromCart({{ item.id }})">
            <i class="fa-solid fa-trash-can"></i> Remove
          </button>
        </div>
        <div style="text-align:right; flex-shrink:0;">
          <p style="font-weight:800; font-size:1.05rem; color:var(--clr-primary-dark);">
            ₹{{ item.subtotal }}
          </p>
        </div>
      </div>
      {% endfor %}
    </div>

    <!-- Summary -->
    <div>
      {% if subtotal < 799 %}
      <div class="free-del-banner">
        🚚 Add ₹{{ 799|add:"-"|add:subtotal }} more for <strong>FREE Delivery</strong>!
        <div style="background:#ddd; border-radius:4px; height:6px; margin-top:6px;">
          <div style="background:var(--clr-primary); height:6px; border-radius:4px; width:{% widthratio subtotal 799 100 %}%;"></div>
        </div>
      </div>
      {% else %}
      <div class="free-del-banner" style="background:#d4edda; border-color:#28a745; color:#155724;">
        🎉 You've unlocked <strong>FREE Delivery</strong>!
      </div>
      {% endif %}

      <div class="summary-card">
        <h3 style="font-weight:700; margin-bottom:16px;">Order Summary</h3>
        <div class="summary-row"><span>Subtotal</span><span>₹{{ subtotal }}</span></div>
        <div class="summary-row">
          <span>Delivery</span>
          <span>
            {% if delivery_charge == 0 %}
              <s style="color:#999;">₹49</s> <span style="color:var(--clr-primary);font-weight:700;">FREE</span>
            {% else %}
              ₹{{ delivery_charge }}
            {% endif %}
          </span>
        </div>
        <div class="summary-total"><span>Total</span><span>₹{{ total }}</span></div>
        <a href="/checkout/" class="btn btn-primary btn-full" style="margin-top:20px; padding:14px; font-size:1rem;">
          Proceed to Checkout →
        </a>
        <a href="/shop/" class="btn btn-outline-primary btn-full" style="margin-top:10px;">
          Continue Shopping
        </a>
        <a href="https://wa.me/917599342112?text=Hi!%20I%20want%20to%20place%20an%20order%20for%20₹{{ total }}"
           class="btn btn-whatsapp btn-full" style="margin-top:10px;" target="_blank">
          Order via WhatsApp
        </a>
      </div>
    </div>
  </div>

  {% else %}
  <div style="text-align:center; padding:80px 20px;">
    <div style="font-size:5rem; margin-bottom:16px;">🛒</div>
    <h2 style="font-weight:700; color:var(--clr-text-dark);">Your cart is empty</h2>
    <p style="color:var(--clr-text-medium); margin-top:8px;">Looks like you haven't added anything yet!</p>
    <a href="/shop/" class="btn btn-primary" style="margin-top:24px; padding:14px 32px;">
      Start Shopping →
    </a>
  </div>
  {% endif %}
</div>

<script>
async function updateCartQty(itemId, qty) {
  if (qty < 1) { removeFromCart(itemId); return; }
  const res = await fetch('/cart/update/', {
    method:'POST',
    headers:{'Content-Type':'application/json','X-CSRFToken':window.KIRANA_CONFIG.csrfToken},
    body: JSON.stringify({item_id: itemId, quantity: qty})
  });
  if (res.ok) location.reload();
}
async function removeFromCart(itemId) {
  const res = await fetch('/cart/remove/', {
    method:'POST',
    headers:{'Content-Type':'application/json','X-CSRFToken':window.KIRANA_CONFIG.csrfToken},
    body: JSON.stringify({item_id: itemId})
  });
  if (res.ok) {
    const el = document.getElementById('cart-item-'+itemId);
    if (el) { el.style.opacity='0'; el.style.transform='scale(0.9)'; el.style.transition='all 0.3s'; setTimeout(()=>location.reload(), 300); }
  }
}
</script>
{% endblock %}
"""

# Write all templates
created = 0
for path, content in TEMPLATES.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    created += 1
    print(f"  [OK] {path}")

print(f"\n✅ {created} templates created/updated")

/**
 * js/cart/cart_ui.js
 * ──────────────────────────────────────────────────────────────────
 * Cart UI layer:
 *   • Floating cart drawer  (open / close / toggle)
 *   • Cart badge count      (live update)
 *   • Mini cart item render (name, qty, price, remove)
 *   • Add-to-cart animation (button → ripple)
 * ──────────────────────────────────────────────────────────────────
 */

/* ================================================================
   FLOATING CART DRAWER
   ================================================================ */

/**
 * Open the floating cart drawer.
 */
function openCartDrawer() {
  const drawer  = document.getElementById('floating-cart');
  const overlay = document.getElementById('cart-overlay');
  if (!drawer) return;

  drawer.classList.add('open');
  if (overlay) overlay.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Refresh cart contents
  refreshCartDrawer();
}

/**
 * Close the floating cart drawer.
 */
function closeCartDrawer() {
  const drawer  = document.getElementById('floating-cart');
  const overlay = document.getElementById('cart-overlay');
  if (!drawer) return;

  drawer.classList.remove('open');
  if (overlay) overlay.classList.remove('active');
  document.body.style.overflow = '';
}

/**
 * Toggle cart drawer.
 */
function toggleCartDrawer(e) {
  if (e) e.preventDefault();
  const drawer = document.getElementById('floating-cart');
  if (!drawer) {
    // No drawer on mobile → navigate to cart page
    window.location.href = '/cart/';
    return;
  }
  drawer.classList.contains('open') ? closeCartDrawer() : openCartDrawer();
}

window.openCartDrawer  = openCartDrawer;
window.closeCartDrawer = closeCartDrawer;
window.toggleCartDrawer = toggleCartDrawer;


/* ================================================================
   CART BADGE — update count in navbar
   ================================================================ */

/**
 * Update all cart badge elements on the page.
 * @param {number} count
 */
function updateCartBadge(count) {
  const badges = document.querySelectorAll('#cart-count, .cart-badge, [data-cart-count]');
  badges.forEach(b => {
    b.textContent = count;
    b.style.display = count > 0 ? 'flex' : 'none';
  });
}

window.updateCartBadge = updateCartBadge;


/* ================================================================
   FETCH & RENDER CART DRAWER CONTENTS
   ================================================================ */

async function refreshCartDrawer() {
  const body = document.getElementById('cart-drawer-body');
  const totalEl = document.getElementById('cart-drawer-total');
  if (!body) return;

  body.innerHTML = `<div style="text-align:center;padding:40px;color:#aaa;">
    <div style="font-size:2rem">🛒</div><p>Loading cart…</p></div>`;

  try {
    const res  = await fetch('/cart/data/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await res.json();

    if (!data.items || data.items.length === 0) {
      body.innerHTML = `
        <div style="text-align:center;padding:40px 20px;color:#aaa;">
          <div style="font-size:3rem;margin-bottom:12px;">🛒</div>
          <p style="font-weight:600;margin-bottom:8px;">Your cart is empty</p>
          <a href="/shop/" style="color:var(--clr-primary);font-weight:700;text-decoration:none;">
            Continue Shopping →
          </a>
        </div>`;
      if (totalEl) totalEl.textContent = '₹0';
      updateCartBadge(0);
      return;
    }

    // Render items
    body.innerHTML = data.items.map(item => `
      <div class="cart-drawer-item" data-item-id="${item.id}">
        <img src="${item.image || '/static/images/icons/placeholder.png'}"
             alt="${item.name}" class="cart-drawer-img"
             onerror="this.src='/static/images/icons/placeholder.png'">
        <div class="cart-drawer-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-meta">
            <div class="cart-item-qty-wrap">
              <button class="qty-btn" onclick="cartQtyChange(${item.id}, -1)">−</button>
              <span class="qty-num">${item.quantity}</span>
              <button class="qty-btn" onclick="cartQtyChange(${item.id}, +1)">+</button>
            </div>
            <span class="cart-item-price">₹${item.subtotal}</span>
          </div>
        </div>
        <button class="cart-remove-btn" onclick="removeCartItem(${item.id})" title="Remove">×</button>
      </div>
    `).join('');

    if (totalEl) totalEl.textContent = `₹${data.total}`;
    updateCartBadge(data.total_items);

  } catch (err) {
    console.error('[Cart] refreshCartDrawer error:', err);
    body.innerHTML = `<div style="text-align:center;padding:40px;color:#ff4757;">
      <p>Failed to load cart. <a href="/cart/">View cart page →</a></p></div>`;
  }
}

window.refreshCartDrawer = refreshCartDrawer;


/* ================================================================
   CART QUANTITY CHANGE
   ================================================================ */

async function cartQtyChange(itemId, delta) {
  try {
    const data = await window.apiPost('/cart/update/', { item_id: itemId, delta });
    if (data.success) {
      updateCartBadge(data.cart_count);
      refreshCartDrawer();
    } else {
      window.showToast(data.message || 'Could not update cart.', 'error');
    }
  } catch (err) {
    console.error('[Cart] cartQtyChange error:', err);
  }
}

async function removeCartItem(itemId) {
  try {
    const data = await window.apiPost('/cart/remove/', { item_id: itemId });
    if (data.success) {
      updateCartBadge(data.cart_count);
      refreshCartDrawer();
      window.showToast('Item removed from cart.', 'info');
    }
  } catch (err) {
    console.error('[Cart] removeCartItem error:', err);
  }
}

window.cartQtyChange   = cartQtyChange;
window.removeCartItem  = removeCartItem;


/* ================================================================
   ADD-TO-CART BUTTON — ripple + success state
   ================================================================ */

/**
 * Animate the "Add to Cart" button after successful add.
 * @param {HTMLElement} btn
 */
function animateAddToCart(btn) {
  if (!btn) return;
  const original = btn.innerHTML;
  btn.innerHTML  = '✅ Added!';
  btn.classList.add('added');
  btn.disabled = true;

  setTimeout(() => {
    btn.innerHTML = original;
    btn.classList.remove('added');
    btn.disabled = false;
  }, 1800);
}

window.animateAddToCart = animateAddToCart;


/* ================================================================
   INIT — wire up cart nav button
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // Cart nav button — navigate directly to cart page (drawer is for floating btn only)
  // No click override needed — the <a href="/cart/"> handles navigation natively

  // Overlay click closes drawer
  const overlay = document.getElementById('cart-overlay');
  if (overlay) {
    overlay.addEventListener('click', closeCartDrawer);
  }

  // Close button inside drawer
  const closeBtn = document.getElementById('cart-drawer-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeCartDrawer);
  }

  // Initialize badge from server-rendered count
  const badge = document.getElementById('cart-count');
  if (badge) {
    const count = parseInt(badge.textContent || '0');
    if (count === 0) badge.style.display = 'none';
  }

  // Inject cart drawer styles if not present
  injectCartStyles();
});


/* ================================================================
   INJECT CART DRAWER CSS
   ================================================================ */
function injectCartStyles() {
  if (document.getElementById('cart-ui-styles')) return;
  const style = document.createElement('style');
  style.id = 'cart-ui-styles';
  style.textContent = `
    .cart-drawer-item {
      display: flex; align-items: center; gap: 12px;
      padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    .cart-drawer-img {
      width: 52px; height: 52px; border-radius: 10px;
      object-fit: cover; background: rgba(255,255,255,0.05); flex-shrink: 0;
    }
    .cart-drawer-info { flex: 1; min-width: 0; }
    .cart-item-name {
      font-weight: 600; font-size: .9rem;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .cart-item-meta {
      display: flex; align-items: center;
      justify-content: space-between; margin-top: 6px;
    }
    .cart-item-qty-wrap {
      display: flex; align-items: center; gap: 8px;
    }
    .qty-btn {
      width: 26px; height: 26px; border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.06);
      color: inherit; cursor: pointer; font-size: 1rem; line-height: 1;
      display: flex; align-items: center; justify-content: center;
    }
    .qty-btn:hover { background: var(--clr-primary); border-color: var(--clr-primary); color: #fff; }
    .qty-num { font-weight: 700; min-width: 22px; text-align: center; }
    .cart-item-price { font-weight: 800; color: var(--clr-primary); font-size: .95rem; }
    .cart-remove-btn {
      background: none; border: none; color: #ff4757;
      font-size: 1.3rem; cursor: pointer; padding: 4px; flex-shrink: 0;
      border-radius: 6px; line-height: 1;
    }
    .cart-remove-btn:hover { background: rgba(255,71,87,.12); }
    .btn.added { background: #2ed573 !important; }
  `;
  document.head.appendChild(style);
}

console.log('[Kirana] cart_ui.js loaded ✓');

/**
 * js/cart/cart_manager.js
 * ──────────────────────────────────────────────────────────────────
 * Cart business logic:
 *   • addToCart(productId, qty)   — AJAX POST to /cart/add/
 *   • updateCartItem(id, qty)     — AJAX POST to /cart/update/
 *   • removeFromCart(id)          — AJAX POST to /cart/remove/
 *   • getCartCount()              — GET  /cart/count/
 *   • Product-card buttons wired on DOMContentLoaded
 * ──────────────────────────────────────────────────────────────────
 */

/* ================================================================
   CORE ACTIONS
   ================================================================ */

/**
 * Add a product to the cart.
 * @param {number|string} productId
 * @param {number} qty – default 1
 * @param {HTMLElement|null} btnEl – optional button element to animate
 */
async function addToCart(productId, qty = 1, btnEl = null) {
  if (!window.KIRANA_CONFIG?.isAuthenticated) {
    window.showToast('Please login to add items to cart 🔐', 'warning');
    setTimeout(() => {
      window.location.href = '/auth/login/?next=' + encodeURIComponent(window.location.pathname);
    }, 1200);
    return;
  }

  try {
    const data = await window.apiPost('/cart/add/', { product_id: productId, quantity: qty });

    if (data.success) {
      window.updateCartBadge(data.cart_count);
      window.showToast(`${data.product_name || 'Item'} added to cart! 🛒`, 'success');
      if (btnEl) window.animateAddToCart(btnEl);
    } else {
      window.showToast(data.message || 'Could not add to cart.', 'error');
    }
  } catch (err) {
    console.error('[Cart] addToCart error:', err);
    window.showToast('Network error. Please try again.', 'error');
  }
}

/**
 * Update quantity of a cart item.
 * @param {number} itemId  – CartItem PK
 * @param {number} delta   – +1 or -1
 */
async function updateCartItem(itemId, delta) {
  try {
    const data = await window.apiPost('/cart/update/', { item_id: itemId, delta });
    if (data.success) {
      window.updateCartBadge(data.cart_count);
      if (window.refreshCartDrawer) window.refreshCartDrawer();
    } else {
      window.showToast(data.message || 'Update failed.', 'error');
    }
  } catch (err) {
    console.error('[Cart] updateCartItem error:', err);
  }
}

/**
 * Remove a cart item completely.
 * @param {number} itemId
 */
async function removeFromCart(itemId) {
  try {
    const data = await window.apiPost('/cart/remove/', { item_id: itemId });
    if (data.success) {
      window.updateCartBadge(data.cart_count);
      if (window.refreshCartDrawer) window.refreshCartDrawer();
      window.showToast('Item removed from cart.', 'info');
    }
  } catch (err) {
    console.error('[Cart] removeFromCart error:', err);
  }
}

/**
 * Fetch the current cart item count and refresh badge.
 */
async function getCartCount() {
  try {
    const res  = await fetch('/cart/count/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await res.json();
    window.updateCartBadge(data.count || 0);
    return data.count || 0;
  } catch {
    return 0;
  }
}

// Expose globally
window.addToCart      = addToCart;
window.updateCartItem = updateCartItem;
window.removeFromCart = removeFromCart;
window.getCartCount   = getCartCount;


/* ================================================================
   WIRE PRODUCT-CARD "ADD TO CART" BUTTONS
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // Delegate to handle dynamically loaded cards too
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-add-to-cart]');
    if (!btn) return;

    e.preventDefault();
    const productId = btn.dataset.addToCart;

    // Find quantity input inside card or wrapper
    const card = btn.closest('[data-product-card], .product-card-actions, .product-card, .product-detail-actions, .product-detail-info');
    let qty = 1;
    if (card) {
      const qtyInput = card.querySelector('[data-qty], .qty-input, input[name="quantity"]');
      if (qtyInput) {
        qty = parseInt(qtyInput.value) || 1;
      }
    } else if (btn.dataset.qty) {
      qty = parseInt(btn.dataset.qty) || 1;
    }

    addToCart(productId, qty, btn);
  });

  // Quantity +/- on cart page (full page, not drawer)
  document.body.addEventListener('click', (e) => {
    const incBtn = e.target.closest('[data-qty-increase]');
    const decBtn = e.target.closest('[data-qty-decrease]');
    const remBtn = e.target.closest('[data-cart-remove]');

    if (incBtn) updateCartItem(incBtn.dataset.qtyIncrease, +1);
    if (decBtn) updateCartItem(decBtn.dataset.qtyDecrease, -1);
    if (remBtn) removeFromCart(remBtn.dataset.cartRemove);
  });
});

/**
 * changeQty — used by product card +/- qty buttons (onclick="changeQty(this, ±1)")
 * Finds the nearest .qty-input relative to the clicked button and updates its value.
 * @param {HTMLElement} btn  - the clicked +/- button
 * @param {number}      delta - +1 or -1
 */
function changeQty(btn, delta) {
  const wrapper = btn.closest('.qty-selector');
  if (!wrapper) return;
  const input = wrapper.querySelector('[data-qty]') || wrapper.querySelector('.qty-input');
  if (!input) return;

  let val = parseInt(input.value) || 1;
  const min = parseInt(input.min) || 1;
  const max = parseInt(input.max) || 99;

  val = Math.min(Math.max(val + delta, min), max);
  input.value = val;
}

window.changeQty = changeQty;

console.log('[Kirana] cart_manager.js loaded ✓');

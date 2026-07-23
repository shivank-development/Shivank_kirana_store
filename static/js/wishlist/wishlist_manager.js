/**
 * js/wishlist/wishlist_manager.js
 * ──────────────────────────────────────────────────────────────────
 * Wishlist business logic:
 *   • toggleWishlist(productId, btnEl)  — POST /wishlist/toggle/
 *   • loadWishlistCount()               — GET  /wishlist/count/
 *   • Wire all [data-wishlist-toggle] buttons
 * ──────────────────────────────────────────────────────────────────
 */

/**
 * Toggle a product in / out of wishlist.
 * @param {number|string} productId
 * @param {HTMLElement|null} btnEl – the heart icon element
 */
async function toggleWishlist(productId, btnEl = null) {
  if (!window.KIRANA_CONFIG?.isAuthenticated) {
    window.showToast('Please login to use Wishlist ❤️', 'warning');
    setTimeout(() => {
      window.location.href = '/auth/login/?next=' + encodeURIComponent(window.location.pathname);
    }, 1200);
    return;
  }

  try {
    const data = await window.apiPost(`/wishlist/toggle/${productId}/`);

    if (data.success) {
      const inWishlist = data.is_wishlisted;

      window.showToast(
        inWishlist ? `Added to Wishlist ❤️` : `Removed from Wishlist`,
        inWishlist ? 'success' : 'info'
      );

      // Update all buttons matching this product
      document.querySelectorAll(`[data-wishlist-toggle="${productId}"]`).forEach(btn => {
        if (inWishlist) {
          btn.classList.add('wishlisted');
          // FontAwesome: switch regular → solid
          const icon = btn.querySelector('i') || btn;
          icon.classList.remove('fa-regular');
          icon.classList.add('fa-solid');
          btn.style.color = '#e91e63';
        } else {
          btn.classList.remove('wishlisted');
          const icon = btn.querySelector('i') || btn;
          icon.classList.remove('fa-solid');
          icon.classList.add('fa-regular');
          btn.style.color = '';

          // If on wishlist page → reload page
          if (window.location.pathname.includes('/wishlist/')) {
            window.location.reload();
          }
        }
      });

    } else {
      window.showToast(data.message || 'Error updating wishlist.', 'error');
    }
  } catch (err) {
    console.error('[Wishlist] toggleWishlist error:', err);
    window.showToast('Network error. Please try again.', 'error');
  }
}

/**
 * Fetch wishlist count and update badge/heart in navbar.
 */
async function loadWishlistCount() {
  try {
    const res  = await fetch('/wishlist/count/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await res.json();
    const badge = document.getElementById('wishlist-count');
    if (badge) {
      badge.textContent = data.count || 0;
      badge.style.display = (data.count > 0) ? 'flex' : 'none';
    }
  } catch {}
}

window.toggleWishlist    = toggleWishlist;
window.loadWishlistCount = loadWishlistCount;


/* ================================================================
   WIRE ALL WISHLIST BUTTONS ON PAGE
   ================================================================ */
document.addEventListener('DOMContentLoaded', () => {
  // Delegate so dynamically loaded product cards also work
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-wishlist-toggle]');
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    const productId = btn.dataset.wishlistToggle;
    toggleWishlist(productId, btn);
  });

  // Init count badge
  if (window.KIRANA_CONFIG?.isAuthenticated) {
    loadWishlistCount();
  }
});

console.log('[Kirana] wishlist_manager.js loaded ✓');

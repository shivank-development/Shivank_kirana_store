/**
 * js/ajax/cart_ajax.js
 * ──────────────────────────────────────────────────────────────────
 * Cart specific AJAX handlers (e.g., Coupon code application).
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  const couponForm = document.getElementById('coupon-form');
  const couponInput = document.getElementById('coupon-input');
  const couponBtn = document.getElementById('apply-coupon-btn');
  const discountRow = document.getElementById('discount-row');
  const totalEl = document.getElementById('cart-final-total');

  if (couponForm && couponInput && couponBtn) {
    couponForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const code = couponInput.value.trim();
      if (!code) return;

      couponBtn.disabled = true;
      couponBtn.innerHTML = 'Applying...';

      try {
        const res = await window.apiPost('/cart/apply-coupon/', { code });
        
        if (res.success) {
          window.showToast?.('Coupon applied successfully! 🎉', 'success');
          
          if (discountRow) {
            discountRow.style.display = 'flex';
            discountRow.querySelector('.discount-amount').textContent = `- ₹${res.discount_amount}`;
          }
          if (totalEl) totalEl.textContent = `₹${res.new_total}`;
          
          couponBtn.innerHTML = 'Applied';
          couponBtn.classList.add('btn-success');
        } else {
          window.showToast?.(res.message || 'Invalid coupon code.', 'error');
          couponBtn.disabled = false;
          couponBtn.innerHTML = 'Apply';
        }
      } catch (err) {
        window.showToast?.('Network error.', 'error');
        couponBtn.disabled = false;
        couponBtn.innerHTML = 'Apply';
      }
    });
  }
});

console.log('[Kirana] cart_ajax.js loaded ✓');

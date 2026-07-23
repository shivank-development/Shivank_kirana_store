/**
 * js/checkout/upi_payment.js
 * ──────────────────────────────────────────────────────────────────
 * Handles the UPI payment verification via UTR submission.
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  const verifyForm = document.getElementById('upi-verify-form');
  const utrInput = document.getElementById('utr-input');
  const verifyBtn = document.getElementById('verify-btn');
  
  if (verifyForm) {
    verifyForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const utr = utrInput.value.trim();
      const orderId = verifyForm.dataset.orderId;
      
      if (utr.length < 12) {
        window.showToast?.('Please enter a valid 12-digit UTR number.', 'warning');
        return;
      }

      verifyBtn.disabled = true;
      verifyBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Verifying...';

      try {
        const res = await window.apiPost(`/checkout/verify-upi/${orderId}/`, { utr: utr });
        
        if (res.success) {
          window.showToast?.('Payment recorded successfully!', 'success');
          setTimeout(() => {
            window.location.href = `/checkout/success/${orderId}/`;
          }, 1000);
        } else {
          window.showToast?.(res.message || 'Verification failed.', 'error');
          verifyBtn.disabled = false;
          verifyBtn.innerHTML = 'Verify Payment';
        }
      } catch (err) {
        console.error('UPI Verification error:', err);
        window.showToast?.('Network error. Please try again.', 'error');
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = 'Verify Payment';
      }
    });
  }
});

console.log('[Kirana] upi_payment.js loaded ✓');

/**
 * js/checkout/cod_handler.js
 * ──────────────────────────────────────────────────────────────────
 * Handles COD confirmation (call / advance payment).
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  const confirmCallBtn = document.getElementById('cod-confirm-call-btn');
  const confirmAdvanceBtn = document.getElementById('cod-advance-btn');

  if (confirmCallBtn) {
    confirmCallBtn.addEventListener('click', async () => {
      const orderId = confirmCallBtn.dataset.orderId;
      confirmCallBtn.disabled = true;
      confirmCallBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

      try {
        const res = await window.apiPost(`/checkout/cod/call-confirm/${orderId}/`);
        if (res.success) {
          window.showToast?.('We will call you shortly to confirm the order.', 'success');
          setTimeout(() => { window.location.href = `/checkout/success/${orderId}/`; }, 2000);
        } else {
          window.showToast?.(res.message || 'Error processing request.', 'error');
          confirmCallBtn.disabled = false;
          confirmCallBtn.innerHTML = 'Confirm by Call';
        }
      } catch (e) {
        window.showToast?.('Network error.', 'error');
        confirmCallBtn.disabled = false;
        confirmCallBtn.innerHTML = 'Confirm by Call';
      }
    });
  }

  if (confirmAdvanceBtn) {
    confirmAdvanceBtn.addEventListener('click', () => {
      // Logic to show QR code or redirect to advance payment gateway
      const orderId = confirmAdvanceBtn.dataset.orderId;
      window.location.href = `/checkout/cod/advance-pay/${orderId}/`;
    });
  }
});

console.log('[Kirana] cod_handler.js loaded ✓');

/**
 * js/admin/payment_actions.js
 * ──────────────────────────────────────────────────────────────────
 * Admin payment approval/rejection
 * ──────────────────────────────────────────────────────────────────
 */

async function updatePaymentStatus(paymentId, status) {
  if (!confirm(`Are you sure you want to ${status} this payment?`)) return;
  
  try {
    const res = await window.apiPost(`/admin-panel/payments/update-status/${paymentId}/`, { status });
    if (res.success) {
      window.showToast?.(`Payment ${status} successfully.`, 'success');
      setTimeout(() => window.location.reload(), 1000);
    } else {
      window.showToast?.(res.message || 'Error updating payment', 'error');
    }
  } catch (err) {
    window.showToast?.('Network error', 'error');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-payment-action]');
    if (!btn) return;
    
    e.preventDefault();
    const paymentId = btn.dataset.paymentId;
    const action = btn.dataset.paymentAction; // 'approved', 'rejected'
    
    updatePaymentStatus(paymentId, action);
  });
});

console.log('[Kirana] admin/payment_actions.js loaded ✓');

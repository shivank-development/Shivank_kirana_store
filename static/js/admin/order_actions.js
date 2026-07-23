/**
 * js/admin/order_actions.js
 * ──────────────────────────────────────────────────────────────────
 * Admin order status updates (Deliver, Cancel, Pack, etc.)
 * ──────────────────────────────────────────────────────────────────
 */

async function updateOrderStatus(orderId, status) {
  if (!confirm(`Are you sure you want to change status to ${status}?`)) return;
  
  try {
    const res = await window.apiPost(`/admin-panel/orders/update-status/${orderId}/`, { status });
    if (res.success) {
      window.showToast?.(`Order ${orderId} marked as ${status}.`, 'success');
      setTimeout(() => window.location.reload(), 1000);
    } else {
      window.showToast?.(res.message || 'Error updating status', 'error');
    }
  } catch (err) {
    window.showToast?.('Network error', 'error');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-order-action]');
    if (!btn) return;
    
    e.preventDefault();
    const orderId = btn.dataset.orderId;
    const action = btn.dataset.orderAction; // 'packed', 'shipped', 'delivered', 'cancelled'
    
    updateOrderStatus(orderId, action);
  });
});

console.log('[Kirana] admin/order_actions.js loaded ✓');

/**
 * js/checkout/checkout_flow.js
 * ──────────────────────────────────────────────────────────────────
 * Checkout page logic:
 *   • Address selection
 *   • Payment method selection
 *   • Place Order button handling
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  const placeOrderBtn = document.getElementById('place-order-btn');
  const paymentOptions = document.querySelectorAll('input[name="payment_method"]');
  const addressRadios = document.querySelectorAll('input[name="address_id"]');

  if (placeOrderBtn) {
    placeOrderBtn.addEventListener('click', async (e) => {
      e.preventDefault();

      const selectedAddress = document.querySelector('input[name="address_id"]:checked');
      const selectedPayment = document.querySelector('input[name="payment_method"]:checked');

      if (!selectedAddress) {
        window.showToast?.('Please select a delivery address.', 'warning');
        return;
      }
      if (!selectedPayment) {
        window.showToast?.('Please select a payment method.', 'warning');
        return;
      }

      placeOrderBtn.disabled = true;
      placeOrderBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

      try {
        const payload = {
          address_id: selectedAddress.value,
          payment_method: selectedPayment.value
        };

        const res = await window.apiPost('/checkout/place-order/', payload);
        
        if (res.success) {
          if (selectedPayment.value === 'UPI') {
            window.location.href = `/checkout/upi/${res.order_id}/`;
          } else {
            // COD
            window.location.href = `/checkout/success/${res.order_id}/`;
          }
        } else {
          window.showToast?.(res.message || 'Error placing order.', 'error');
          placeOrderBtn.disabled = false;
          placeOrderBtn.innerHTML = 'Place Order';
        }
      } catch (err) {
        console.error('Order placement error:', err);
        window.showToast?.('Network error. Please try again.', 'error');
        placeOrderBtn.disabled = false;
        placeOrderBtn.innerHTML = 'Place Order';
      }
    });
  }

  // Address selection styling
  addressRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.address-card').forEach(c => c.classList.remove('selected'));
      radio.closest('.address-card').classList.add('selected');
    });
  });
});

console.log('[Kirana] checkout_flow.js loaded ✓');

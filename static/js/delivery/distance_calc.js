/**
 * js/delivery/distance_calc.js
 * ──────────────────────────────────────────────────────────────────
 * Pincode / Distance checking for delivery availability.
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  const pincodeInput = document.getElementById('pincode-input');
  const checkBtn = document.getElementById('pincode-check-btn');
  const resultDiv = document.getElementById('pincode-result');

  if (checkBtn && pincodeInput) {
    checkBtn.addEventListener('click', async () => {
      const pin = pincodeInput.value.trim();
      if (!window.isValidPincode?.(pin)) {
        if(resultDiv) {
            resultDiv.innerHTML = '<span class="text-danger"><i class="fa-solid fa-circle-xmark"></i> Invalid 6-digit Pincode</span>';
        }
        return;
      }

      checkBtn.disabled = true;
      checkBtn.innerHTML = 'Checking...';

      try {
        const res = await fetch(`/delivery/check-pincode/?pincode=${pin}`);
        const data = await res.json();

        if(resultDiv) {
            if (data.available) {
                resultDiv.innerHTML = `<span style="color:#2ed573"><i class="fa-solid fa-circle-check"></i> Delivery available. Time: ${data.eta}</span>`;
            } else {
                resultDiv.innerHTML = `<span class="text-danger"><i class="fa-solid fa-circle-xmark"></i> Sorry, we do not deliver to this pincode yet.</span>`;
            }
        }
      } catch (err) {
        if(resultDiv) resultDiv.innerHTML = '<span class="text-danger">Network error.</span>';
      } finally {
        checkBtn.disabled = false;
        checkBtn.innerHTML = 'Check';
      }
    });
  }
});

console.log('[Kirana] distance_calc.js loaded ✓');

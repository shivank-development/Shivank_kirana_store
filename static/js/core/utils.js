/**
 * js/core/utils.js
 * ──────────────────────────────────────────────────────────────────
 * Shared utility functions available globally:
 *   • getCsrfToken()       — read CSRF cookie
 *   • apiPost(url, body)   — JSON POST with CSRF header
 *   • showToast(msg, type) — toast notification
 *   • shareProduct(url, title) — Web Share API / clipboard fallback
 *   • formatPrice(n)       — "₹1,299"
 *   • debounce(fn, ms)     — debounce wrapper
 *   • formatTimeAgo(dateStr) — "2h ago"
 *   • copyToClipboard(text)  — async clipboard copy
 * ──────────────────────────────────────────────────────────────────
 */

/* ── CSRF ── */
function getCsrfToken() {
  const m = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : '';
}

/* ── JSON POST ── */
async function apiPost(url, body = {}) {
  const res = await fetch(url, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
    body:    JSON.stringify(body),
  });
  return res.json();
}

/* ── TOAST ── */
function showToast(msg, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;flex-direction:column;gap:10px;pointer-events:none;';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const colors = { success: '#2ed573', error: '#ff4757', warning: '#ffa502', info: '#74b9ff' };

  const toast = document.createElement('div');
  toast.style.cssText = `
    display:flex;align-items:center;gap:10px;padding:12px 18px;border-radius:12px;
    font-size:.92rem;font-weight:600;background:#fff;color:#1a1a1a;
    box-shadow:0 8px 24px rgba(0,0,0,.15);pointer-events:all;
    border-left:4px solid ${colors[type]||colors.success};
    max-width:320px;animation:slideInToast .3s ease;
  `;
  toast.innerHTML = `
    <span style="font-size:1.1rem;">${icons[type]||'🔔'}</span>
    <span style="flex:1;">${msg}</span>
    <button onclick="this.parentElement.remove()" style="background:none;border:none;cursor:pointer;color:#aaa;font-size:1.2rem;line-height:1;">×</button>
  `;

  // Inject keyframe once
  if (!document.getElementById('toast-kf')) {
    const st = document.createElement('style');
    st.id = 'toast-kf';
    st.textContent = `@keyframes slideInToast{from{transform:translateX(60px);opacity:0}to{transform:translateX(0);opacity:1}}`;
    document.head.appendChild(st);
  }

  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

/* ── SHARE PRODUCT ── */
async function shareProduct(url, title, text) {
  url   = url   || window.location.href;
  title = title || document.title;
  text  = text  || 'Check out this product on Shivank Kirana Store!';

  if (navigator.share) {
    try {
      await navigator.share({ title, text, url });
      return;
    } catch (e) {
      if (e.name === 'AbortError') return; // user cancelled
    }
  }
  // Fallback: copy link
  await copyToClipboard(url);
  showToast('Link copied to clipboard! 📋', 'success');
}

/* ── CLIPBOARD ── */
async function copyToClipboard(text) {
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(text);
  } else {
    const el = document.createElement('textarea');
    el.value = text;
    el.style.position = 'fixed';
    el.style.opacity  = '0';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    el.remove();
  }
}

/* ── FORMAT PRICE ── */
function formatPrice(n) {
  return '₹' + Number(n).toLocaleString('en-IN');
}

/* ── DEBOUNCE ── */
function debounce(fn, ms = 300) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

/* ── TIME AGO ── */
function formatTimeAgo(dateStr) {
  const diff = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (diff < 60)    return 'just now';
  if (diff < 3600)  return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

/* ── PINCODE VALIDATION ── */
function isValidPincode(pin) {
  return /^\d{6}$/.test(String(pin).trim());
}

/* ── EXPORT GLOBALLY ── */
window.getCsrfToken    = getCsrfToken;
window.apiPost         = apiPost;
window.showToast       = showToast;
window.shareProduct    = shareProduct;
window.copyToClipboard = copyToClipboard;
window.formatPrice     = formatPrice;
window.debounce        = debounce;
window.formatTimeAgo   = formatTimeAgo;
window.isValidPincode  = isValidPincode;

console.log('[Kirana] utils.js loaded ✓');

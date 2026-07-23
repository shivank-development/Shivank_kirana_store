/**
 * js/core/app.js
 * ──────────────────────────────────────────────────────────────────
 * Core application bootstrap:
 *   • Category sidebar toggle  (toggleSidebar / closeSidebar)
 *   • Mobile hamburger menu    (toggleMobileMenu)
 *   • User account dropdown    (hover / click)
 *   • Nav-dropdown hovers      (Snacks, Chocolates, etc.)
 *   • Sticky navbar shadow     (scroll)
 *   • WhatsApp pre-fill        (dynamic message)
 *   • Notification Bell        (dropdown open/close)
 *   • Global CSRF helper       (getCsrfToken)
 * ──────────────────────────────────────────────────────────────────
 */

/* ================================================================
   0.  GLOBAL HELPERS
   ================================================================ */

/**
 * Read a cookie value by name (used for CSRF token).
 */
function getCsrfToken() {
  const name   = 'csrftoken';
  const match  = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : '';
}

/**
 * Simple fetch wrapper that always includes CSRF and returns JSON.
 */
async function apiPost(url, body = {}) {
  const res = await fetch(url, {
    method:  'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken':  getCsrfToken(),
    },
    body: JSON.stringify(body),
  });
  return res.json();
}

/**
 * Show a toast notification at bottom-right.
 * @param {string} msg
 * @param {'success'|'error'|'warning'|'info'} type
 */
function showToast(msg, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || '🔔'}</span>
    <span class="toast-msg">${msg}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">×</button>
  `;

  container.appendChild(toast);
  // Auto-remove after 4 s
  setTimeout(() => toast.remove(), 4000);
}

// Expose globally so other modules can use it
window.showToast    = showToast;
window.getCsrfToken = getCsrfToken;
window.apiPost      = apiPost;


/* ================================================================
   1.  STICKY NAVBAR — add shadow on scroll
   ================================================================ */
(function initNavbarScroll() {
  const navbar = document.getElementById('main-navbar');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });
})();


/* ================================================================
   2.  CATEGORY SIDEBAR (All Categories ≡)
   ================================================================ */

/**
 * Toggle the left-side category drawer.
 * Called by: <button onclick="toggleSidebar()"> in navbar.html
 */
function toggleSidebar() {
  const sidebar = document.getElementById('category-sidebar');
  const overlay = document.getElementById('category-sidebar-overlay');
  if (!sidebar) return;

  const isOpen = sidebar.classList.toggle('open');
  if (overlay) overlay.classList.toggle('active', isOpen);

  // Rotate chevron on the button
  const chev = document.querySelector('.nav-categories-btn .chev');
  if (chev) chev.style.transform = isOpen ? 'rotate(180deg)' : '';

  // Prevent body scroll when sidebar open on mobile
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

/**
 * Close sidebar explicitly (called by overlay click, close btn, etc.).
 */
function closeSidebar() {
  const sidebar = document.getElementById('category-sidebar');
  const overlay = document.getElementById('category-sidebar-overlay');
  if (!sidebar) return;

  sidebar.classList.remove('open');
  if (overlay) overlay.classList.remove('active');

  const chev = document.querySelector('.nav-categories-btn .chev');
  if (chev) chev.style.transform = '';

  document.body.style.overflow = '';
}

// Close sidebar on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeSidebar();
    closeMobileMenu();
    closeNotificationDropdown();
  }
});

// Expose globally
window.toggleSidebar = toggleSidebar;
window.closeSidebar  = closeSidebar;


/* ================================================================
   3.  MOBILE HAMBURGER MENU
   ================================================================ */

function toggleMobileMenu() {
  const menu    = document.getElementById('mobile-menu');
  const overlay = document.getElementById('mobile-overlay');
  const btn     = document.getElementById('hamburger-btn');
  if (!menu) return;

  const isOpen = menu.classList.toggle('open');
  if (overlay) overlay.classList.toggle('active', isOpen);
  if (btn)     btn.classList.toggle('active', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function closeMobileMenu() {
  const menu    = document.getElementById('mobile-menu');
  const overlay = document.getElementById('mobile-overlay');
  const btn     = document.getElementById('hamburger-btn');
  if (!menu) return;

  menu.classList.remove('open');
  if (overlay) overlay.classList.remove('active');
  if (btn)     btn.classList.remove('active');
  document.body.style.overflow = '';
}

window.toggleMobileMenu = toggleMobileMenu;
window.closeMobileMenu  = closeMobileMenu;


/* ================================================================
   4.  USER ACCOUNT DROPDOWN
   ================================================================ */
(function initUserDropdown() {
  const userWrap = document.querySelector('.user-dropdown-wrap');
  if (!userWrap) return;

  const dropdown = userWrap.querySelector('.nav-dropdown');
  const btn      = userWrap.querySelector('.user-btn');
  if (!dropdown || !btn) return;

  // Desktop: toggle on click
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isActive = userWrap.classList.toggle('active');
    btn.setAttribute('aria-expanded', isActive);
  });

  // Close when clicking outside
  document.addEventListener('click', () => {
    userWrap.classList.remove('active');
    btn.setAttribute('aria-expanded', 'false');
  });
})();


/* ================================================================
   5.  MEGA DROPDOWN (Snacks, Chocolates, etc.)
   ================================================================ */
(function initMegaDropdowns() {
  const wraps = document.querySelectorAll('.nav-dropdown-wrap:not(.user-dropdown-wrap)');
  wraps.forEach(wrap => {
    const dropdown = wrap.querySelector('.nav-dropdown');
    if (!dropdown) return;

    let timer;

    wrap.addEventListener('mouseenter', () => {
      clearTimeout(timer);
      dropdown.classList.add('open');
    });

    wrap.addEventListener('mouseleave', () => {
      timer = setTimeout(() => dropdown.classList.remove('open'), 300);
    });
  });
})();


/* ================================================================
   6.  WHATSAPP — dynamic pre-filled message
   ================================================================ */
(function initWhatsApp() {
  const waBtn = document.querySelector('.whatsapp-btn');
  if (!waBtn) return;

  const number = window.KIRANA_CONFIG?.whatsappNumber || '917599342112';

  // Build context-aware message
  const path = window.location.pathname;
  let msg = 'Hi! I want to place an order from Shivank Kirana Store.';

  if (path.includes('/product/')) {
    const title = document.querySelector('h1.product-title, .product-name');
    if (title) msg = `Hi! I want to order: *${title.textContent.trim()}* from Shivank Kirana Store.`;
  } else if (path.includes('/cart/')) {
    msg = 'Hi! I want to place an order. I have items in my cart.';
  }

  waBtn.href = `https://wa.me/${number}?text=${encodeURIComponent(msg)}`;
})();


/* ================================================================
   7.  NOTIFICATION BELL
   ================================================================ */
(function initNotificationBell() {
  const bell    = document.getElementById('notification-bell-btn');
  const dropdown = document.getElementById('notification-dropdown');
  if (!bell || !dropdown) return;

  bell.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = dropdown.classList.toggle('open');
    bell.setAttribute('aria-expanded', isOpen);

    // Mark notifications read when opened
    if (isOpen && window.KIRANA_CONFIG?.isAuthenticated) {
      fetch('/notifications/mark-read/', {
        method:  'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
      }).then(() => {
        // Clear badge count
        const badge = document.getElementById('notif-badge');
        if (badge) badge.style.display = 'none';
      }).catch(() => {});
    }
  });

  document.addEventListener('click', () => dropdown.classList.remove('open'));
  dropdown.addEventListener('click', (e) => e.stopPropagation());
})();

function closeNotificationDropdown() {
  const dropdown = document.getElementById('notification-dropdown');
  if (dropdown) dropdown.classList.remove('open');
}

window.closeNotificationDropdown = closeNotificationDropdown;


/* ================================================================
   8.  THEME TOGGLE (dark / light) — optional
   ================================================================ */
(function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);

  toggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next    = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
})();


/* ================================================================
   9.  TOAST CSS — inject if not already in stylesheet
   ================================================================ */
(function injectToastStyles() {
  if (document.getElementById('toast-inline-styles')) return;
  const style = document.createElement('style');
  style.id = 'toast-inline-styles';
  style.textContent = `
    #toast-container {
      position: fixed; bottom: 24px; right: 24px;
      z-index: 99999; display: flex; flex-direction: column; gap: 10px;
      pointer-events: none;
    }
    .toast {
      display: flex; align-items: center; gap: 10px;
      padding: 12px 18px; border-radius: 12px;
      font-size: .92rem; font-weight: 600;
      background: #1e2a1e; color: #fff;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      pointer-events: all;
      animation: slideInToast .3s ease;
      max-width: 320px;
    }
    .toast-success { border-left: 4px solid #2ed573; }
    .toast-error   { border-left: 4px solid #ff4757; }
    .toast-warning { border-left: 4px solid #ffa502; }
    .toast-info    { border-left: 4px solid #74b9ff; }
    .toast-close   { margin-left: auto; background: none; border: none; color: #aaa; cursor: pointer; font-size: 1.2rem; line-height: 1; }
    @keyframes slideInToast {
      from { transform: translateX(60px); opacity: 0; }
      to   { transform: translateX(0);    opacity: 1; }
    }
  `;
  document.head.appendChild(style);
})();


console.log('[Kirana] app.js loaded ✓');

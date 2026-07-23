/**
 * js/search/search_handler.js
 * ──────────────────────────────────────────────────────────────────
 * Search bar logic:
 *   • Live autocomplete suggestions via AJAX  (/search/autocomplete/)
 *   • Keyboard navigation (↑ ↓ Enter Escape)
 *   • Recent searches (localStorage)
 *   • Submit → /search/?q=…
 * ──────────────────────────────────────────────────────────────────
 */

(function SearchHandler() {
  'use strict';

  const RECENT_KEY = 'kirana_recent_searches';
  const MAX_RECENT = 5;
  let   acTimer    = null;

  /* ── DOM refs ── */
  const input      = document.getElementById('navbar-search');
  const dropdown   = document.getElementById('search-autocomplete');
  const form       = input ? input.closest('form') : null;

  if (!input || !dropdown) return;  // not on a page with navbar search

  /* ── Recent searches helpers (Disabled by User Request) ── */
  try {
    localStorage.removeItem(RECENT_KEY);
  } catch(e) {}

  function getRecent() {
    return [];
  }

  function saveRecent(query) {
    // Search history disabled
  }

  /* ── Render dropdown ── */
  function renderDropdown(items, type = 'results') {
    if (!items.length || type === 'recent') {
      closeDropdown();
      return;
    }

    const html = items.map((item, i) => {
      return `<div class="ac-item" role="option" data-query="${escHtml(item.name)}" tabindex="-1">
        <img src="${item.image || '/static/images/icons/placeholder.png'}"
             class="ac-img" alt=""
             onerror="this.src='/static/images/icons/placeholder.png'">
        <div class="ac-info">
          <span class="ac-name">${highlight(item.name, input.value)}</span>
          <span class="ac-price">₹${item.price}</span>
        </div>
        ${item.category ? `<span class="ac-cat">${escHtml(item.category)}</span>` : ''}
      </div>`;
    }).join('');

    dropdown.innerHTML = html;
    dropdown.classList.remove('hidden');
    dropdown.setAttribute('aria-expanded', 'true');

    // Wire click events
    dropdown.querySelectorAll('.ac-item').forEach(el => {
      el.addEventListener('click', (e) => {
        const query = el.dataset.query;
        input.value = query;
        closeDropdown();
        form.submit();
      });
    });
  }

  function closeDropdown() {
    dropdown.classList.add('hidden');
    dropdown.setAttribute('aria-expanded', 'false');
    dropdown.innerHTML = '';
  }

  function showRecent() {
    closeDropdown();
  }

  /* ── Highlight matching part ── */
  function highlight(text, query) {
    if (!query) return escHtml(text);
    const re = new RegExp(`(${escRe(query)})`, 'gi');
    return escHtml(text).replace(re, '<mark class="ac-highlight">$1</mark>');
  }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function escRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /* ── Fetch suggestions ── */
  async function fetchSuggestions(q) {
    try {
      const res  = await fetch(`/search/autocomplete/?q=${encodeURIComponent(q)}`,
        { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      const data = await res.json();
      renderDropdown(data.results || [], 'results');
    } catch {
      closeDropdown();
    }
  }

  /* ── Input events ── */
  input.addEventListener('input', () => {
    const q = input.value.trim();
    clearTimeout(acTimer);

    if (q.length < 2) {
      closeDropdown();
      return;
    }

    acTimer = setTimeout(() => fetchSuggestions(q), 280);
  });

  input.addEventListener('focus', () => {
    if (input.value.trim().length < 2) closeDropdown();
  });

  /* ── Keyboard navigation ── */
  input.addEventListener('keydown', (e) => {
    const items = [...dropdown.querySelectorAll('.ac-item')];
    const cur   = dropdown.querySelector('.ac-item.focused');
    const idx   = items.indexOf(cur);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (cur) cur.classList.remove('focused');
      const next = items[idx + 1] || items[0];
      if (next) { next.classList.add('focused'); input.value = next.dataset.query; }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (cur) cur.classList.remove('focused');
      const prev = items[idx - 1] || items[items.length - 1];
      if (prev) { prev.classList.add('focused'); input.value = prev.dataset.query; }
    } else if (e.key === 'Escape') {
      closeDropdown();
    } else if (e.key === 'Enter') {
      if (cur) {
        e.preventDefault();
        input.value = cur.dataset.query;
        saveRecent(cur.dataset.query);
        closeDropdown();
        form.submit();
      }
    }
  });

  /* ── Form submit → save recent ── */
  if (form) {
    form.addEventListener('submit', () => {
      const q = input.value.trim();
      if (q) saveRecent(q);
    });
  }

  /* ── Close on outside click ── */
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      closeDropdown();
    }
  });

  /* ── Inject styles ── */
  (function injectACStyles() {
    if (document.getElementById('ac-styles')) return;
    const s = document.createElement('style');
    s.id = 'ac-styles';
    s.textContent = `
      .search-autocomplete {
        position: absolute; top: calc(100% + 6px); left: 0; right: 0;
        background: var(--clr-surface, #1e2a1e);
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 14px; box-shadow: 0 16px 40px rgba(0,0,0,.4);
        z-index: 9999; overflow: hidden; max-height: 380px; overflow-y: auto;
      }
      .search-autocomplete.hidden { display: none; }
      .ac-item {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 16px; cursor: pointer; transition: background .15s;
        font-size: .92rem;
      }
      .ac-item:hover, .ac-item.focused { background: rgba(255,255,255,.07); }
      .ac-img { width: 40px; height: 40px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
      .ac-icon { width: 20px; text-align: center; flex-shrink: 0; }
      .ac-info { flex: 1; min-width: 0; }
      .ac-name { font-weight: 600; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .ac-price { color: var(--clr-primary, #2a7f2a); font-weight: 700; font-size: .85rem; }
      .ac-cat { font-size: .75rem; color: #aaa; white-space: nowrap; }
      .ac-del { margin-left: auto; background: none; border: none; color: #aaa; cursor: pointer; font-size: 1.1rem; padding: 2px 6px; border-radius: 4px; }
      .ac-del:hover { background: rgba(255,71,87,.15); color: #ff4757; }
      .ac-highlight { background: rgba(26,93,26,.35); color: var(--clr-primary, #2a7f2a); border-radius: 2px; }
      .search-input-wrap { position: relative; }
    `;
    document.head.appendChild(s);
  })();

  console.log('[Kirana] search_handler.js loaded ✓');
})();

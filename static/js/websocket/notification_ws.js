/**
 * js/websocket/notification_ws.js
 * ──────────────────────────────────────────────────────────────────
 * Notification Bell:
 *   • WebSocket connection to ws://…/ws/notifications/
 *   • Fallback: long-poll via /notifications/unread/ every 30 s
 *   • Renders notification dropdown items
 *   • Updates unread badge count
 *   • Mark-all-read on bell open
 * ──────────────────────────────────────────────────────────────────
 */

(function NotificationWS() {
  'use strict';

  // Only run for authenticated users
  if (!window.KIRANA_CONFIG?.isAuthenticated) return;

  const POLL_INTERVAL = 8_000;  // 8 s fast poll for instant updates

  let ws          = null;
  let pollTimer   = null;
  let unreadCount = 0;

  /* ── DOM ── */
  const badge    = document.getElementById('notif-badge');
  const list     = document.getElementById('notification-list');
  const bellBtn  = document.getElementById('notification-bell-btn');

  /* ================================================================
     BADGE UPDATE
     ================================================================ */
  function setUnreadBadge(count) {
    unreadCount = count;
    if (!badge) return;
    if (count > 0) {
      badge.textContent = count > 99 ? '99+' : count;
      badge.style.display = 'inline-flex';
    } else {
      badge.style.display = 'none';
    }
  }

  /* ================================================================
     RENDER NOTIFICATION LIST
     ================================================================ */
  function renderNotifications(notifications) {
    if (!list) return;

    if (!notifications || notifications.length === 0) {
      list.innerHTML = `
        <div class="notif-empty" style="text-align:center;padding:32px 16px;color:#aaa;">
          <div style="font-size:2.2rem;margin-bottom:6px;">🔔</div>
          <p style="margin:0;font-size:.85rem;font-weight:600;">No unread notifications</p>
        </div>`;
      return;
    }

    list.innerHTML = notifications.map(n => `
      <div class="notif-item ${n.is_read ? '' : 'unread'}" data-id="${n.id}" onclick="handleNotifClick('${n.id}', '${n.action_url || ''}')" style="display:flex;align-items:flex-start;gap:12px;padding:12px 16px;border-bottom:1px solid #f0f0f0;cursor:pointer;background:${n.is_read ? '#fff' : '#f4fbf4'};">
        <div class="notif-icon-wrap ${n.type || 'default'}" style="width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;background:#e8f5e9;">
          ${getNotifIcon(n.type)}
        </div>
        <div class="notif-body" style="flex:1;min-width:0;">
          <div class="notif-title" style="font-weight:700;font-size:.88rem;color:#1a3a1a;margin-bottom:2px;">${escHtml(n.title || '')}</div>
          <div class="notif-msg" style="font-size:.8rem;color:#555;line-height:1.4;">${escHtml(n.message || '')}</div>
          <div class="notif-time" style="font-size:.72rem;color:#aaa;margin-top:4px;">${timeAgo(n.created_at)}</div>
        </div>
        ${!n.is_read ? '<div class="notif-dot" style="width:8px;height:8px;border-radius:50%;background:#226b2e;flex-shrink:0;margin-top:5px;"></div>' : ''}
      </div>
    `).join('');
  }

  window.handleNotifClick = function(id, url) {
    const csrfToken = window.getCsrfToken ? window.getCsrfToken() : '';
    fetch(`/notifications/${id}/read/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
    }).catch(() => {});

    if (url) {
      window.location.href = url;
    }
  };

  function getNotifIcon(type) {
    const map = {
      order:    '📦',
      payment:  '💳',
      delivery: '🚴',
      stock:    '⚠️',
      promo:    '🎁',
      default:  '🔔',
    };
    return map[type] || map.default;
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function timeAgo(dateStr) {
    if (!dateStr) return '';
    const diff = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
    if (diff < 30)   return 'just now';
    if (diff < 60)   return `${diff}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }

  /* ================================================================
     FETCH UNREAD (HTTP fallback / initial load)
     ================================================================ */
  async function fetchUnread() {
    try {
      const res  = await fetch('/notifications/unread/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      if (!res.ok) return;
      const data = await res.json();
      const newCount = data.count || 0;
      if (newCount > unreadCount && unreadCount > 0) {
        // Show subtle notification sound / toast if new notification arrived
        if (data.notifications && data.notifications[0]) {
          window.showToast?.(data.notifications[0].title, 'info');
        }
      }
      setUnreadBadge(newCount);
      renderNotifications(data.notifications || []);
    } catch {}
  }

  /* ================================================================
     MARK ALL READ
     ================================================================ */
  async function markAllRead() {
    try {
      // Mark each unread notification read individually
      const unreadItems = document.querySelectorAll('.notif-item.unread[data-id]');
      const csrfToken   = window.getCsrfToken ? window.getCsrfToken() : '';
      for (const el of unreadItems) {
        const id = el.dataset.id;
        fetch(`/notifications/${id}/read/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
        }).catch(() => {});
      }
      setUnreadBadge(0);
      // Update visual dots
      document.querySelectorAll('.notif-item.unread').forEach(el => {
        el.classList.remove('unread');
        el.querySelector('.notif-dot')?.remove();
      });
    } catch {}
  }

  /* ================================================================
     WEBSOCKET
     ================================================================ */
  function connectWS() {
    const userId   = window.KIRANA_CONFIG?.userId;
    if (!userId) { startPolling(); return; }
    const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
    const url      = `${protocol}://${location.host}/ws/notifications/${userId}/`;

    try {
      ws = new WebSocket(url);
    } catch {
      startPolling();
      return;
    }

    ws.onopen = () => {
      console.log('[Notif WS] connected ✓');
      clearInterval(pollTimer);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === 'notification') {
          // New notification received
          setUnreadBadge(unreadCount + 1);
          // Show toast popup
          window.showToast?.(`${msg.data?.title || 'New notification'}`, 'info');
          // Re-fetch list
          fetchUnread();
        } else if (msg.type === 'unread_count') {
          setUnreadBadge(msg.count || 0);
        }
      } catch {}
    };

    ws.onclose = () => {
      console.log('[Notif WS] closed — switching to polling');
      ws = null;
      startPolling();
    };

    ws.onerror = () => {
      ws?.close();
      startPolling();
    };
  }

  function startPolling() {
    if (pollTimer) return;
    pollTimer = setInterval(fetchUnread, POLL_INTERVAL);
  }

  /* ================================================================
     BELL BUTTON — mark read on open
     ================================================================ */
  if (bellBtn) {
    bellBtn.addEventListener('click', () => {
      if (unreadCount > 0) {
        markAllRead();
      }
    });
  }

  /* ================================================================
     INJECT STYLES
     ================================================================ */
  (function injectStyles() {
    if (document.getElementById('notif-ws-styles')) return;
    const s = document.createElement('style');
    s.id = 'notif-ws-styles';
    s.textContent = `
      #notification-dropdown {
        position: absolute; top: calc(100% + 10px); right: 0;
        width: 340px; max-height: 480px;
        background: var(--clr-surface, #1e2a1e);
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,.4);
        z-index: 9999; overflow: hidden;
        display: none; flex-direction: column;
      }
      #notification-dropdown.open { display: flex; }
      .notif-dropdown-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 14px 18px;
        border-bottom: 1px solid rgba(255,255,255,.07);
        font-weight: 700; font-size: .95rem;
      }
      .notif-mark-read-btn {
        background: none; border: none; color: var(--clr-primary, #2a7f2a);
        font-size: .8rem; cursor: pointer; font-weight: 600;
      }
      #notification-list { overflow-y: auto; max-height: 380px; }
      .notif-empty { text-align: center; padding: 40px 20px; color: #aaa; }
      .notif-item {
        display: flex; align-items: flex-start; gap: 12px;
        padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,.05);
        cursor: pointer; transition: background .15s;
        position: relative;
      }
      .notif-item:hover { background: rgba(255,255,255,.04); }
      .notif-item.unread { background: rgba(26,93,26,.06); }
      .notif-icon-wrap {
        width: 38px; height: 38px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; flex-shrink: 0;
        background: rgba(255,255,255,.07);
      }
      .notif-icon-wrap.order    { background: rgba(116,185,255,.15); }
      .notif-icon-wrap.payment  { background: rgba(162,155,254,.15); }
      .notif-icon-wrap.delivery { background: rgba(255,165,2,.15); }
      .notif-icon-wrap.promo    { background: rgba(46,213,115,.15); }
      .notif-body { flex: 1; min-width: 0; }
      .notif-title { font-weight: 600; font-size: .88rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .notif-msg   { font-size: .8rem; color: #aaa; margin-top: 2px; line-height: 1.4;
                     display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
      .notif-time  { font-size: .73rem; color: #666; margin-top: 4px; }
      .notif-dot   { width: 8px; height: 8px; border-radius: 50%; background: var(--clr-primary, #2a7f2a); flex-shrink: 0; margin-top: 4px; }
      /* Bell button relative positioning */
      .notif-bell-wrap { position: relative; }
      #notif-badge {
        position: absolute; top: -4px; right: -6px;
        min-width: 18px; height: 18px; padding: 0 4px;
        background: #ff4757; color: #fff;
        border-radius: 20px; font-size: .68rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        line-height: 1;
      }
    `;
    document.head.appendChild(s);
  })();

  /* ================================================================
     INIT
     ================================================================ */
  // Try WebSocket; fall back to polling if it fails
  if ('WebSocket' in window) {
    connectWS();
  } else {
    startPolling();
  }

  // Initial fetch on page load
  fetchUnread();

  console.log('[Kirana] notification_ws.js loaded ✓');
})();

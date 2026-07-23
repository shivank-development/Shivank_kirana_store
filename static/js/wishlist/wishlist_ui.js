document.addEventListener('DOMContentLoaded', () => {
  // --- Wishlist Toggle Logic ---
  const toggleButtons = document.querySelectorAll('[data-wishlist-toggle]');
  
  toggleButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation(); // prevent clicking through to product detail page
      
      const productId = btn.dataset.wishlistToggle;
      
      try {
        const res = await fetch(`/wishlist/toggle/${productId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          }
        });
        
        const data = await res.json();
        
        if (data.success) {
          // Toggle heart icon UI
          if (data.is_wishlisted) {
            btn.classList.remove('fa-regular');
            btn.classList.add('fa-solid');
            btn.style.color = '#e91e63';
          } else {
            btn.classList.remove('fa-solid');
            btn.classList.add('fa-regular');
            btn.style.color = ''; // reset to default CSS color
            
            // If we are on the wishlist page, reload the page after removal
            if (window.location.pathname.includes('/wishlist/')) {
              window.location.reload();
            }
          }
          
          // Show toast notification
          if (window.showToast) window.showToast(data.message, 'success');
        } else {
          // Handle error (e.g. Please login)
          if(res.status === 401) {
             window.location.href = '/auth/login/?next=' + window.location.pathname;
          } else {
            if (window.showToast) window.showToast(data.message || 'Something went wrong', 'error');
          }
        }
      } catch (err) {
        console.error('Error toggling wishlist:', err);
      }
    });
  });
});

// Helper for CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

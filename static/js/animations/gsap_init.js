/**
 * js/animations/gsap_init.js
 * ──────────────────────────────────────────────────────────────────
 * GSAP ScrollTrigger animations for UI elements.
 * ──────────────────────────────────────────────────────────────────
 */

document.addEventListener('DOMContentLoaded', () => {
  // Only init if GSAP is loaded
  if (typeof gsap === 'undefined') return;
  
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // Navbar animation on load
  gsap.from('.navbar-main', {
    y: -100,
    opacity: 0,
    duration: 0.8,
    ease: 'power3.out'
  });

  // Fade up elements on scroll
  const fadeUpElements = document.querySelectorAll('.fade-up');
  fadeUpElements.forEach(el => {
    gsap.from(el, {
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none none'
      },
      y: 40,
      opacity: 0,
      duration: 0.8,
      ease: 'power3.out'
    });
  });

  // Staggered product cards (Removed because it causes cards to get stuck at low opacity)
  // if you still want animations, use standard CSS transitions.
});

console.log('[Kirana] gsap_init.js loaded ✓');

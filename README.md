# Premium Short Video Platform (TikTok / Reels Clone)

## 1. Project Overview
This project is a production-ready, startup-quality frontend for a short-form video platform similar to TikTok, Instagram Reels, and YouTube Shorts. The objective is to deliver a highly optimized, accessible, and visually stunning web application. 

By combining a **premium luxury dark theme with gold/purple highlights** and a **rich feature set** (stories, timelines, custom sounds, video editors), this template serves as a complete foundation for any modern video-first social network.

---

## 2. Design Philosophy
Our design philosophy revolves around **Premium Engagement**. We aim to create a space that feels expensive, smooth, and highly interactive.

- **Immersive First:** Content takes precedence. UI elements should float seamlessly over or around the video content, using glassmorphism for legibility without breaking immersion.
- **Micro-Interactions:** Every action (like, share, hover) is rewarded with a satisfying, high-framerate animation.
- **Visual Hierarchy:** Subtle contrasts, rather than loud borders, define sections.
- **Premium Feel:** We steer clear of basic grays and flat blacks, favoring deep, rich secondary tones and glowing, energetic accents.

---

## 3. Design System
This project utilizes a custom, heavily curated design system. We rely on **CSS Variables** for easy theming and consistency. The system prioritizes a **luxury dark aesthetic** while maintaining extreme functional depth. 

All UI components adhere to predefined sets of spacing, typography, and motion rules. 

---

## 4. Color Palette
Colors are managed via CSS variables in `variables.css`.

| Role | Color | Hex Code |
| :--- | :--- | :--- |
| **Primary BG** | Deep Black | `#09090B` |
| **Secondary BG** | Dark Navy/Gray | `#121218` |
| **Card BG** | Surface | `#1A1A23` |
| **Card Hover** | Surface Highlight | `#232330` |
| **Primary Accent** | Vibrant Purple | `#7C5CFF` |
| **Secondary Accent** | Neon Blue | `#00D4FF` |
| **Premium Accent** | Gold | `#FFB800` |
| **Success** | Emerald Green | `#00E676` |
| **Danger** | Vibrant Red | `#FF4D6D` |
| **Warning** | Orange | `#FF9800` |
| **Border / Glass** | Translucent White | `rgba(255, 255, 255, 0.08)` |
| **Primary Text** | Pure White | `#FFFFFF` |
| **Secondary Text** | Soft Gray | `#B5B5C3` |
| **Muted Text** | Dim Gray | `#8A8A98` |

---

## 5. Typography
We use robust, modern, sans-serif fonts to ensure clarity and a contemporary feel.

- **Primary Font:** `Poppins` (for Headers, Titles, and premium display elements)
- **Secondary/Body Font:** `Inter` (for paragraphs, descriptions, UI text, and numbers)

### Font Weights
- **Heading:** `700` (Bold)
- **Subheading:** `600` (Semi-Bold)
- **Body:** `400` (Regular)
- **Caption:** `300` (Light)

---

## 6. Icons
Consistent iconography is crucial for a unified UI. We employ a mix of standard libraries and custom SVGs.
- **Core UI:** Bootstrap Icons / Hero Icons
- **Unique Platform Icons:** Custom SVG (e.g., custom Like bursts, verified badges)
- **Socials / Payments:** FontAwesome Brands / Payment Icons

---

## 7. Spacing System
A strict spacing scale ensures vertical and horizontal rhythm. All margins and paddings must align to this 4px/8px baseline.

- `xs` : 4px
- `sm` : 8px
- `md` : 16px
- `lg` : 24px
- `xl` : 32px
- `2xl`: 48px
- `3xl`: 64px

---

## 8. Border Radius
Rounded corners soften the UI and guide the eye naturally.
- **Cards:** `20px`
- **Buttons:** `16px`
- **Inputs:** `14px`
- **Video Containers:** `18px`
- **Avatars:** `50%` (Perfect Circle)
- **Badges / Pills:** `999px` (Fully Rounded)

---

## 9. Shadows
We use subtle, deep shadows rather than harsh drop shadows, creating a layered, floating effect.
- **Small (Buttons/Chips):** `0 4px 10px rgba(0,0,0,.15)`
- **Medium (Cards/Dropdowns):** `0 10px 25px rgba(0,0,0,.25)`
- **Large (Modals/Popovers):** `0 25px 60px rgba(0,0,0,.40)`

---

## 10. Animations
Motion provides feedback and delight. Every interactive element requires motion.
- **Core Transitions:** `Fade In`, `Slide Up`, `Slide Left`, `Slide Right`
- **Interactions:** `Zoom`, `Bounce`, `Pulse`, `Ripple`
- **Special Effects:** 
  - `Like Heart Burst` (When double-tapping a video)
  - `Bookmark Flip` (Saving an item)
  - `Glass Reflection` (On premium cards)
  - `Shimmer` (For skeleton loading states)
  - `Floating Button` (Upload CTA)

---

## 11. Folder Structure
```text
short-video-app/
│
├── index.html
├── splash.html
├── login.html
├── signup.html
├── forgot-password.html
├── otp.html
├── reset-password.html
├── home.html
├── discover.html
├── search.html
├── upload.html
├── editor.html
├── profile.html
├── edit-profile.html
├── creator.html
├── notifications.html
├── messages.html
├── chat.html
├── live.html
├── wallet.html
├── premium.html
├── dashboard.html
├── settings.html
├── admin.html
├── 404.html
├── maintenance.html
│
├── css/
│   ├── variables.css
│   ├── typography.css
│   ├── reset.css
│   ├── utilities.css
│   ├── animations.css
│   ├── components.css
│   ├── layout.css
│   ├── home.css
│   ├── profile.css
│   ├── search.css
│   ├── upload.css
│   ├── editor.css
│   ├── dashboard.css
│   └── responsive.css
│
├── js/
│   ├── app.js
│   ├── auth.js
│   ├── home.js
│   ├── search.js
│   ├── discover.js
│   ├── upload.js
│   ├── editor.js
│   ├── profile.js
│   ├── notification.js
│   ├── message.js
│   ├── wallet.js
│   ├── dashboard.js
│   ├── settings.js
│   ├── validation.js
│   ├── animation.js
│   └── helper.js
│
└── assets/
    ├── images/
    ├── avatars/
    ├── thumbnails/
    ├── reels/
    ├── stories/
    ├── videos/
    ├── icons/
    ├── lottie/
    ├── gif/
    ├── sounds/
    ├── fonts/
    └── bootstrap/
```

---

## 12. Images Guide
All static imagery should be optimized (WebP preferred) and stored in `assets/images/`.
- **Logos:** `logo-dark.png`, `logo-light.png`, `logo-icon.svg`, `splash-logo.png`
- **Illustrations:** `login-illustration.png`, `signup-illustration.png`, `empty-search.svg`, `404.svg`, `maintenance.svg`
- **Banners:** `wallet-banner.jpg`, `premium-banner.jpg`, `creator-banner.jpg`
- **Placeholders:** `upload-placeholder.png`, `profile-cover-default.jpg`, `video-placeholder.jpg`

---

## 13. Videos Guide
Categorized structural folders for platform video content.
- `travel/` (`travel1.mp4`, etc.)
- `gaming/` (`game1.mp4`, etc.)
- `music/`, `comedy/`, `technology/`, `education/`, `sports/`

---

## 14. Avatar Guide
Standardized profile pictures for mockup testing.
- `user1.jpg`, `user2.jpg`, `user3.jpg`
- `creator1.jpg`, `creator2.jpg`, `creator3.jpg`
- `verified.png` (Verification Badge)
- `default-avatar.png` (Fallback)

---

## 15. Icons Guide
Essential SVGs required across the application:
- **Interaction:** Like, Comment, Bookmark, Share, Gift, Follow
- **Navigation:** Home, Discover, Search, Profile, Upload, Notification, Messages, Wallet, Settings
- **Media/Hardware:** Camera, Gallery, Microphone, Music, Location
- **Status/Actions:** Verified, Premium, Edit, Delete, Report, Block, Download, Language, Theme, Logout

---

## 16. Component Library
Reusable UI components constructed combining `layout.css`, `components.css`, and `variables.css`.
- **Layout:** Navbar, Bottom Navigation, Sticky Header
- **Media:** Video Player, Video Card, Story Carousel, Music Tile
- **Interactive:** Comment Sheet, Share Modal, Gift Animation, Live Chat Panel
- **Data/Display:** Profile Card, Creator Card, Statistics Card, Analytics Chart, Pricing Card, Wallet Card
- **System:** Skeleton Loader, Empty State, Error State, Toast Notification, Confirmation Modal

---

## 17. Every HTML Page
- **Auth Flow:** `login.html`, `signup.html`, `forgot-password.html`, `otp.html`, `reset-password.html`
- **Main Feed:** `index.html`, `splash.html`, `home.html` (Reels feed)
- **Discovery:** `discover.html`, `search.html` (Search by Users, Videos, Sounds, Hashtags)
- **Creation:** `upload.html`, `editor.html` (Timeline editor, crop, filters)
- **User Space:** `profile.html`, `edit-profile.html`, `creator.html`
- **Engagement:** `notifications.html`, `messages.html`, `chat.html`, `live.html`
- **Monetization & Settings:** `wallet.html`, `premium.html`, `dashboard.html`, `settings.html`, `admin.html`
- **System:** `404.html`, `maintenance.html`

---

## 18. Every CSS File
Modular CSS architecture for maintainability.
- `variables.css`: Colors, spacing, typography scales.
- `reset.css`: CSS normalization.
- `typography.css`: Font families and text styles.
- `utilities.css`: Helper classes (margins, paddings, flex).
- `animations.css`: Keyframes for all transitions and interactions.
- `components.css`: Buttons, cards, inputs.
- `layout.css`: Navbars, grids, wrappers.
- `home.css`, `profile.css`, `search.css`, `upload.css`, `editor.css`, `dashboard.css`: Page-specific styles.
- `responsive.css`: Media queries for breakpoints.

---

## 19. Every JS File
Modular, single-responsibility JavaScript.
- `auth.js`: Login, Signup, OTP logic.
- `home.js`: Infinite Scroll, Auto Play/Pause, Double Tap to Like.
- `editor.js`: Video Trim, Split, Crop, Filter application.
- `search.js`: Live Search, Suggestions, Trending logic.
- `dashboard.js`: Analytics charting.
- `settings.js`: Theme toggling, Localization.
- `animation.js`: Scroll triggers, custom loaders.
- `helper.js`: Date formatting, API wrappers, LocalStorage managers.

---

## 20. Bootstrap Usage
While custom CSS is preferred for the premium look, Bootstrap (Grid System & Utilities only) can be utilized to rapidly build responsive column structures (e.g., in the `dashboard.html` or `settings.html`). **Do not use default Bootstrap buttons, navbars, or cards**, as they will override the luxury custom design system.

---

## 21. Responsive Breakpoints
Mobile-first approach. All interfaces must scale perfectly up to 4K.
- `320px` (Small Mobile)
- `375px` (Standard Mobile - iPhone)
- `425px` (Large Mobile)
- `576px` (Small Tablets)
- `768px` (Tablets / iPads)
- `992px` (Small Laptops)
- `1200px` (Desktops)
- `1400px` (Large Screens)
- `1600px` (Ultra Wide)
- `1920px` (Full HD / 4K monitors)

---

## 22. Accessibility (a11y)
The application must be fully accessible.
- **ARIA Labels:** All icon-only buttons must have descriptive `aria-label` tags.
- **Keyboard Navigation:** Forms, modals, and the video feed must be navigable via `Tab`, `Arrow Up/Down`, and `Spacebar`.
- **Contrast Ratios:** Ensure text on `Secondary Text` (`#B5B5C3`) passes WCAG AA contrast against `Primary BG` (`#09090B`).

---

## 23. Performance Rules
Short-video platforms demand extreme performance.
- **Lazy Loading:** Videos and images outside the immediate viewport must be lazy-loaded.
- **Preloading:** The *next* video in the scroll queue should preload metadata and the first 2 seconds of video.
- **DOM Size:** Old videos that have scrolled far out of view should be unmounted or recycled to prevent memory leaks.
- **Asset Optimization:** Use `.webp` for images and compressed `.mp4`/`.webm` for videos.

---

## 24. SEO
For pages like `profile.html` and public `video` views:
- **Meta Tags:** Open Graph tags for rich previews on iMessage/WhatsApp/Twitter.
- **Semantic HTML:** Use `<main>`, `<article>`, `<section>`, `<nav>`, `<aside>`.
- **Alt Text:** Ensure all images and thumbnails have descriptive alt text.

---

## 25. Loading States
Never show a blank white screen.
- **Skeletons:** Use `shimmer` skeleton loaders mimicking the exact shape of the content (cards, profile details).
- **Splash Screen:** Display a branded Lottie animation or floating logo on initial app load.

---

## 26. Empty States
Empty states should be beautiful and actionable.
- **No Videos:** Show an illustration and a "Start Uploading" primary button.
- **No Messages:** Friendly ghost/inbox graphic urging users to start a chat.
- **Empty Search:** Suggestions of trending hashtags or creators.

---

## 27. Error States
Provide graceful failure modes.
- **Network Disconnect:** Toast notification sliding down from the top ("You're offline").
- **404 Page:** Custom `404.html` with a cosmic/lost graphic and a button back home.
- **Failed Upload:** Provide a retry mechanism right on the upload card.

---

## 28. Future Features
Planned enhancements post-MVP:
- WebRTC Live Streaming (`live.html` capabilities).
- AR Face Filters within the browser using WebGL.
- Advanced E-commerce integration directly within the video feed (Shoppable Reels).
- In-depth Creator analytics with exportable CSVs.
- Advanced audio mixing in `editor.js`.

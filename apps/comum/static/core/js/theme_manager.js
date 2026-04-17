/* ============================================================
   SIGE — Theme Hub Manager v3.0
   Rebuilt for Premium Switcher Component
   Supports curated themes: Indigo, Cinza, Azul
============================================================ */

(() => {
  const STORAGE_KEY = 'sige_theme';
  const THEMES = new Set([
    'indigo-profundo',
    'cinza-industrial',
    'azul-corporativo'
  ]);

  let initialized = false;

  /**
   * Applies theme to document and persists to localStorage
   */
  function applyTheme(theme) {
    const t = THEMES.has(theme) ? theme : 'indigo-profundo';
    document.documentElement.setAttribute('data-theme', t);
    
    // Update active state in UI
    document.querySelectorAll('.theme-option').forEach(opt => {
      opt.classList.toggle('current', opt.dataset.theme === t);
    });

    try {
      localStorage.setItem(STORAGE_KEY, t);
    } catch (e) {
      console.warn('Storage blocked:', e);
    }
    return t;
  }

  /**
   * Initializes the Hub logic (clicks, toggles, sync)
   */
  function initThemeHub() {
    if (initialized) return;
    
    const trigger = document.getElementById('theme-hub-trigger');
    const panel = document.getElementById('theme-hub-panel');
    const options = document.querySelectorAll('.theme-option');

    if (!trigger || !panel) return;
    initialized = true;

    // 1. Toggle Panel
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      panel.classList.toggle('active');
    });

    // 2. Close Panel on outside click
    document.addEventListener('click', (e) => {
      if (!panel.contains(e.target) && !trigger.contains(e.target)) {
        panel.classList.remove('active');
      }
    });

    // 3. Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') panel.classList.remove('active');
    });

    // 4. Handle Theme Selection
    options.forEach(opt => {
      opt.addEventListener('click', () => {
        const themeToApply = opt.dataset.theme;
        applyTheme(themeToApply);
        
        // Add a "success" micro-animation
        opt.style.transform = 'scale(0.95)';
        setTimeout(() => {
          opt.style.transform = '';
          panel.classList.remove('active');
        }, 150);
      });
    });

    // 5. Initial Sync
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'indigo-profundo';
    applyTheme(currentTheme);
  }

  // Ensure initialization on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeHub);
  } else {
    initThemeHub();
  }
})();

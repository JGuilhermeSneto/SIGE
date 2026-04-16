/* ============================================================
   SIGE — Theme Manager v2.1
   Persists theme + applies to <html data-theme="...">
   Supports 8 complete themes with localStorage persistence
============================================================ */

(() => {
  const STORAGE_KEY = 'sige_theme';
  const THEMES = new Set([
    'indigo-profundo',      // Dark (antigo 'default')
    'cinza-industrial',     // Light Minimal (antigo 'gray')
    'azul-corporativo',     // Corporate Blue with borders
  ]);

  const THEME_NAMES = {
    'indigo-profundo': 'Indigo Profundo',
    'cinza-industrial': 'Cinza Industrial',
    'azul-corporativo': 'Azul Corporativo'
  };

  let initialized = false;

  function applyTheme(theme) {
    const t = THEMES.has(theme) ? theme : 'indigo-profundo';
    document.documentElement.setAttribute('data-theme', t);
    try {
      localStorage.setItem(STORAGE_KEY, t);
    } catch (e) {
      // ignore (privacy modes / restrictive browsers)
    }
    return t;
  }

  function getThemeName(themeId) {
    return THEME_NAMES[themeId] || themeId;
  }

  function initThemeSelector() {
    if (initialized) return;
    initialized = true;

    const select = document.getElementById('theme-select');
    if (!select) return;

    // Clear existing options to prevent duplicates
    select.innerHTML = '';

    // Populate select with all themes (sorted alphabetically)
    Array.from(THEMES).sort().forEach(themeId => {
      const option = document.createElement('option');
      option.value = themeId;
      option.textContent = getThemeName(themeId);
      select.appendChild(option);
    });

    // sync UI with current attribute / localStorage
    let current = document.documentElement.getAttribute('data-theme') || 'indigo-profundo';
    if (!THEMES.has(current)) {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored && THEMES.has(stored)) current = stored;
      } catch (e) {
        // ignore
      }
      current = applyTheme(current);
    }
    select.value = current;

    // Listen for theme changes
    select.addEventListener('change', () => {
      applyTheme(select.value);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initThemeSelector();
  });
})();


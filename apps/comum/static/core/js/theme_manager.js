/* ============================================================
   SIGE — Theme Manager v2.1
   Persists theme + applies to <html data-theme="...">
   Supports 8 complete themes with localStorage persistence
============================================================ */

(() => {
  const STORAGE_KEY = 'sige_theme';
  const THEMES = new Set([
    'indigo-profundo',      // 1. Dark (antigo 'default')
    'brisa-aqua',           // 2. Dark Electric Cyan
    'ceu-sereno',           // 3. Atmospheric Sky Gradient
    'cinza-industrial',     // 4. Light Minimal (antigo 'gray')
    'azul-corporativo',     // 5. Corporate Blue with borders
    'ambar-noite',          // 6. Amber Dark (antigo 'amber')
    'jardim-fosco',         // 7. Botanical Green
    'terra-musgo'           // 8. Sage Green
  ]);

  const THEME_NAMES = {
    'indigo-profundo': 'Indigo Profundo',
    'brisa-aqua': 'Brisa Aqua',
    'ceu-sereno': 'Céu Sereno',
    'cinza-industrial': 'Cinza Industrial',
    'azul-corporativo': 'Azul Corporativo',
    'ambar-noite': 'Âmbar & Noite',
    'jardim-fosco': 'Jardim Fosco',
    'terra-musgo': 'Terra & Musgo'
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


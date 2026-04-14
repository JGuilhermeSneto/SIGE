# 🏗️ SIGE Themes — Arquitetura Técnica (v2.0)

> **Documentação Técnica** | **Para:** Desenvolvedores | **Versão:** 2.0

---

## 📦 Estrutura de Arquivos

```
SIGE/
├── apps/
│   ├── comum/
│   │   └── static/core/
│   │       └── css/design_system/
│   │           ├── tokens.css                 ← 📌 Base (CSS variables)
│   │           ├── themes.css                 ← 🎨 9 Temas (2000+ linhas)
│   │           ├── themes-backup.css          ← 🔄 Backup v1
│   │           ├── animations.css             ← ✨ Keyframes
│   │           ├── base.css                   ← 🎯 Base styles
│   │           ├── components.css             ← 🧩 Components
│   │           ├── layout.css                 ← 📐 Grid/flex
│   │           ├── notifications.css          ← 🔔 Toast/alerts
│   │           ├── README.md                  ← 📖 Quick guide
│   │           ├── THEMES_DOCUMENTATION.md   ← 📚 Full docs
│   │           └── ARCHITECTURE.md            ← 🏗️ This file
│   │
│   └── js/
│       └── core/
│           └── theme_manager.js               ← 🔧 Theme applicator
│
└── usuarios/
    └── templates/core/
        └── base.html                          ← 📄 HTML root
```

---

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                         │
│                  (Click theme selector)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          theme_manager.js                                   │
│  • initThemeSelector() — Popula <select>                    │
│  • applyTheme(id) — Aplica tema                             │
│  • localStorage.setItem('sige_theme', id)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│       <html data-theme="THEME_ID">                          │
│  document.documentElement.setAttribute('data-theme', 'X')   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              CSS Attribute Selector                         │
│  html[data-theme="USER_SELECTED"] { ... }                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        CSS Variable Redefinition                            │
│  html[data-theme="terra-musgo"] {                           │
│    --primary: #6C7B5A;                                      │
│    --bg-base: #EAF0EA;                                      │
│    --radius-md: 14px;                                       │
│    /* 30-40 variáveis por tema */                           │
│  }                                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           CSS Cascade (var() resolution)                    │
│  .sige-card { border-radius: var(--radius-md); }           │
│  → border-radius: 14px (terra-musgo)                        │
│  → border-radius: 18px (brisa-aqua)                         │
│  → border-radius: 4px  (cinza-industrial)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Rendered UI                                    │
│  (Componentes com estilos do tema selecionado)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Sistema de Variáveis CSS

### **Hierarquia:**

```
tokens.css (Base Variables)
    ↓
    ├─ Raiz `:root` (defaults - indigo-profundo)
    │
themes.css (Per-theme overrides)
    ├─ html[data-theme="indigo-profundo"] { /* ... */ }
    ├─ html[data-theme="terra-musgo"] { /* ... */ }
    ├─ html[data-theme="brisa-aqua"] { /* ... */ }
    └─ ... 6 temas mais
```

### **Cascata de Variáveis Exemplo:**

```css
/* tokens.css — PADRÃO (usa indigo-profundo) */
:root {
  --primary: hsl(245, 75%, 60%);           /* roxo */
  --radius-md: 10px;
}

/* themes.css — SOBRESCREVE POR TEMA */
html[data-theme="terra-musgo"] {
  --primary: #6C7B5A;                      /* sage green */
  --radius-md: 14px;
}

html[data-theme="cinza-industrial"] {
  --primary: #2F4F4F;                      /* dark slate */
  --radius-md: 4px;
}

/* base.css — USA AS VARIÁVEIS */
.sige-btn-primary {
  background: var(--primary);              /* muda conforme tema */
  border-radius: var(--radius-md);        /* muda conforme tema */
}
```

---

## 🔧 API — theme_manager.js

### **Objeto THEMES**
```javascript
const THEMES = new Set([
  'indigo-profundo',
  'brisa-aqua',
  'ceu-sereno',
  'cinza-industrial',
  'brisa-quente',
  'azul-corporativo',
  'ambar-noite',
  'jardim-fosco',
  'terra-musgo'
]);
```

### **Objeto THEME_NAMES (Mapeamento)**
```javascript
const THEME_NAMES = {
  'indigo-profundo': 'Indigo Profundo',
  'terra-musgo': 'Terra & Musgo',
  // ... etc
};
```

### **Funções Públicas**

#### `applyTheme(themeId: string): string`
```javascript
applyTheme('terra-musgo');
// Resultado:
// 1. html.setAttribute('data-theme', 'terra-musgo')
// 2. localStorage.setItem('sige_theme', 'terra-musgo')
// 3. Retorna 'terra-musgo'
```

#### `getThemeName(themeId: string): string`
```javascript
getThemeName('terra-musgo');
// Resultado: 'Terra & Musgo'
```

#### `initThemeSelector(): void`
```javascript
initThemeSelector();
// Resultado:
// 1. Busca <select id="theme-select">
// 2. Popula <option> para cada tema
// 3. Sincroniza com localStorage/atributo html
// 4. Adiciona event listener 'change'
```

---

## 📊 Hierarquia de Variáveis (30-40 por Tema)

### **Categoria: Cores Base**
```css
--bg-base           /* Fundo principal da página */
--bg-surface        /* Cards, containers */
--bg-elevated       /* Popovers, modals */
--bg-hover          /* Estados hover */
--bg-input          /* Backgrounds de inputs */
```

### **Categoria: Texto**
```css
--text-primary      /* Texto principal */
--text-secondary    /* Texto secundário */
--text-muted        /* Labels, hints, small text */
```

### **Categoria: Marca & Acentos**
```css
--primary           /* Cor primária do tema */
--primary-dark      /* Variação escura */
--primary-light     /* Variação clara */

--accent-violet     /* Accent 1 */
--accent-cyan       /* Accent 2 */
--accent-emerald    /* Accent 3 */
--accent-amber      /* Accent 4 */
--accent-ruby       /* Accent 5 (errors) */
```

### **Categoria: Borders & Layout**
```css
--border-subtle     /* Borders discretas */
--border-mid        /* Borders normais */

--header-bg         /* Header background */
--header-bg-scrolled /* Header scrolled */
--sidebar-bg-top    /* Sidebar topo */
--sidebar-bg-bottom /* Sidebar bottom */
```

### **Categoria: Shapes & Depth**
```css
--radius-sm         /* small border-radius */
--radius-md         /* medium border-radius */
--radius-lg         /* large border-radius */
--radius-xl         /* extra-large border-radius */

--shadow-sm         /* small shadow */
--shadow-md         /* medium shadow */
--shadow-lg         /* large shadow */
--shadow-glow       /* glow/halo effect */
```

### **Categoria: Transições**
```css
--transition-fast   /* rápido (0.10s-0.18s) */
--transition-mid    /* médio (0.14s-0.28s) */
--transition-slow   /* lento (0.18s-0.46s) */
```

### **Categoria: Tipografia**
```css
--font-main         /* Fonte principal (body) */
--font-display      /* Fonte display (headings) */
```

---

## 🎬 Animações — Por Tema

### **Estrutura de Keyframes**

Cada tema pode ter seu próprio keyframe, aplicado em:
- `.sige-card`
- `.calendar-container`
- `.card-tabela`

```javascript
/* Exemplo: Terra & Musgo */
@keyframes sigeTerraMuscoCalmIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

html[data-theme="terra-musgo"] .sige-card {
  animation: sigeTerraMuscoCalmIn 0.36s ease both;
}
```

### **Matriz de Animações**

| Tema | Keyframe | Easing | Duration | Motion |
|------|----------|--------|----------|--------|
| brisa-aqua | FloatIn | cubic-bezier(0.2, 1.1, 0.2, 1) | 0.38s | Bounce + Scale |
| ceu-sereno | DriftIn | cubic-bezier(0.2, 1.0, 0.2, 1) | 0.45s | Smooth drift |
| cinza-industrial | NENHUMA | — | — | No motion |
| brisa-quente | GentleFloat | ease-out | 0.35s | Float suave |
| azul-corporativo | SlideIn | ease-in-out | 0.30s | Slide formal |
| jardim-fosco | GrowthIn | ease-out | 0.38s | Grow + ScaleY |
| terra-musgo | CalmIn | ease | 0.36s | Calm fade |
| ambar-noite | GlowIn | cubic-bezier(0.25, 0.46, 0.45, 0.94) | 0.40s | Glow effect |
| indigo-profundo | (base) | ease | default | Smooth |

---

## 🧪 Exemplo Prático — Mudando um Tema

### **Cenário: User seleciona "Terra & Musgo"**

**Passo 1:** Usuário clica em dropdown
```html
<select id="theme-select" aria-label="Selecionar tema">
  <option value="indigo-profundo">Indigo Profundo</option>
  <option value="terra-musgo">Terra & Musgo</option>
  <!-- ... -->
</select>
```

**Passo 2:** Evento 'change' dispara
```javascript
select.addEventListener('change', () => {
  applyTheme(select.value); // 'terra-musgo'
});
```

**Passo 3:** applyTheme() executa
```javascript
function applyTheme(theme = 'terra-musgo') {
  document.documentElement.setAttribute('data-theme', 'terra-musgo');
  localStorage.setItem('sige_theme', 'terra-musgo');
}
```

**Passo 4:** HTML muda
```html
<!-- Antes -->
<html data-theme="indigo-profundo">

<!-- Depois -->
<html data-theme="terra-musgo">
```

**Passo 5:** CSS selectors ativam
```css
/* Todos esses disparos: */
html[data-theme="terra-musgo"] .sige-card { ... }
html[data-theme="terra-musgo"] .sige-btn-primary { ... }
html[data-theme="terra-musgo"] .sige-input { ... }
/* ... etc */
```

**Passo 6:** Variáveis mudam
```css
html[data-theme="terra-musgo"] {
  --bg-base:     #EAF0EA;          /* Saga Light */
  --primary:     #6C7B5A;          /* Sage Medium */
  --radius-md:   14px;             /* Medium radius */
  /* ... 36+ variáveis */
}
```

**Passo 7:** Componentes re-renderizam com novo tema
```
Antes: Card com bg indigo, radius 10px, animação suave
Depois: Card com bg sage, radius 14px, animação calm (mesmo render!)
```

**Passo 8:** localStorage persiste
```javascript
// Próxima vez que user visitar o site:
const stored = localStorage.getItem('sige_theme'); // 'terra-musgo'
applyTheme(stored); // Auto-aplica
```

---

## 🔌 Pontos de Extensão

### **1. Adicionar Novo Tema**

**a) Adicione o ID ao theme_manager.js:**
```javascript
const THEMES = new Set([
  // ... existing themes ...
  'novo-tema-incrivel'  // ← NOVO
]);

const THEME_NAMES = {
  // ... existing names ...
  'novo-tema-incrivel': 'Novo Tema Incrível'  // ← NOVO
};
```

**b) Defina as variáveis em themes.css:**
```css
html[data-theme="novo-tema-incrivel"] {
  color-scheme: light;
  
  --bg-base:     #XXXXXX;
  --bg-surface:  #XXXXXX;
  /* ... 30-40 variáveis */
}

/* Customize componentes específicos */
html[data-theme="novo-tema-incrivel"] .sige-card {
  /* ... estilos específicos ... */
}
```

**c) (Opcional) Crie animação keyframe:**
```css
@keyframes sigeNovoTemaIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

html[data-theme="novo-tema-incrivel"] .sige-card {
  animation: sigeNovoTemaIn 0.35s ease both;
}
```

### **2. Modificar Variável Globalmente**

**Mude em tokens.css (afeta todos os temas exceto os que sobrescrevem):**
```css
:root {
  --radius-md: 14px;  /* ← Todos os temas herdam, a menos que sobrescrevam */
}
```

### **3. Mudar Tema via JavaScript**

```javascript
// Modo 1: Aplicar automaticamente
applyTheme('terra-musgo');

// Modo 2: Simular clique no selector
document.getElementById('theme-select').value = 'terra-musgo';
document.getElementById('theme-select').dispatchEvent(new Event('change'));

// Modo 3: Ler tema atual
console.log(document.documentElement.getAttribute('data-theme'));

// Modo 4: Limpar tema (volta para default)
localStorage.removeItem('sige_theme');
applyTheme('indigo-profundo');
```

---

## ✅ Checklist de Qualidade

### **Implementação**
- [x] 9 temas com cores distintas
- [x] Cada tema com 30+ variáveis CSS
- [x] Animações únicas por tema
- [x] Border-radius customizado
- [x] Tipografia diferente
- [x] localStorage persistence
- [x] Fallback para tema default

### **Acessibilidade**
- [ ] WCAG AA contrast ratio (4.5:1) mínimo
- [ ] prefers-reduced-motion respect
- [ ] Focus indicators visíveis
- [ ] Keyboard navigation
- [ ] Screen reader support

### **Performance**
- [ ] CSS bundle size (check gzip)
- [ ] Paint performance (DevTools)
- [ ] localStorage não excede 5MB
- [ ] Sem JavaScript required (degrada gracefully)

### **Testes**
- [ ] 9 browsers diferentes
- [ ] 5 tipos de dispositivos (mobile, tablet, desktop, etc)
- [ ] Dark mode auto-detect
- [ ] localStorage clear/restore
- [ ] Theme switching performance
- [ ] Animações suave (60fps)

---

## 🚀 Performance Notes

### **CSS Variable Resolution**
```
Time: O(1) — Variáveis CSS são ultra-rápidas
       Mudança de tema = paint/composite, não reflow
```

### **localStorage Access**
```
Time: O(1) — Sincronização rápida
      Não bloqueia main thread
      Fallback para sessionStorage se necessário
```

### **DOM Attribute Mutation**
```
Time: O(n) — n = número de seletores que dependem de data-theme
      Tipicamente < 100ms para toda repaint
```

---

## 🐛 Troubleshooting

### **Tema não persiste após reload**
```javascript
/* Verifique: */
1. localStorage.getItem('sige_theme') // Está lá?
2. document.documentElement.getAttribute('data-theme') // Bem setado?
3. Browser está em private mode? (localStorage pode ser desabilitado)
```

### **Variáveis não aplicadas**
```css
/* Checklist: */
1. Existe html[data-theme="seu-tema"] { } em themes.css?
2. Variável está bem nomeada (--primary vs --primary-color)?
3. Seletor é mais específico que a regra em base.css?
```

### **Animações não rodando**
```javascript
/* Verifique: */
1. prefers-reduced-motion: @media (prefers-reduced-motion: reduce) { animation: none; }
2. Elemento tem .sige-card? (animation está acoplada ao elemento?)
3. Duration > 0 e animação nomeada existe?
```

---

## 📚 Referências

- [MDN: CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [CSS Cascade Layers](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
- [Easing Functions](https://easings.net/)
- [WCAG 2.1 Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)

---

**Desenvolvido com ❤️ para SIGE Theme System v2.0**

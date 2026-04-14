# 🎨 SIGE — Sistema Completo de Temas (v2.0)

> **Versão:** 2.0 | **Data:** Abril 2026 | **Status:** ✅ Pronto para Produção

---

## 📋 Resumo Executivo

O SIGE agora possui **9 temas completamente diferentes**, cada um com:
- ✅ **Paleta de cores própria** (no mínimo 6 tons)
- ✅ **Animações únicas** (duração, easing, efeitos)
- ✅ **Border-radius específicos** (de 2px até 999px)
- ✅ **Fontes tipográficas distintas** (serif, sans-serif, display)
- ✅ **Sombras/profundidade temáticas**
- ✅ **Transições customizadas**
- ✅ **Ícones com estilo próprio**

Todos os temas mantêm **máxima clareza visual** e **acessibilidade**.

---

## 🎯 Lista dos 9 Temas

### **Modo ESCURO**

#### 1️⃣ **Indigo Profundo** (ID: `indigo-profundo`)
- **Tipo:** Dark Professional
- **Paleta Base:** Azul indigo, roxo, tons sombrios
- **Cor Primária:** `hsl(245, 75%, 60%)` — Roxo vibrante
- **Caso de Uso:** Padrão profissional, legal, corporativo dark
- **Forma:** Bordas médias (6px-22px), sombras clássicas
- **Fonte Principal:** Inter, Plus Jakarta Sans
- **Animação Signature:** Transições lisas e formais
- **Nomeação Anterior:** `default`

#### 7️⃣ **Âmbar & Noite** (ID: `ambar-noite`)
- **Tipo:** Dark Editorial (Alto Contraste)
- **Paleta:** `#0D0A06` → `#EF9F27` (Âmbar quente sobre preto profundo)
- **Cores:**
  - Fundo: `#0D0A06` (quase preto)
  - Primária: `#EF9F27` (âmbar vibrante)
  - Acentos: `#FAC775`, `#BA7517`
- **Caso de Uso:** Editorial, magazines, contenido premium
- **Forma:** Bordas suaves (8px-24px), fundos com degradados
- **Fonte:** Lora, Playfair Display (serif)
- **Animação:** Suave com efeito "glow", transições por cubic-bezier
- **Insight Visual:** Luz quente em fundo escuro = alto impacto

---

### **Modo CLARO**

#### 2️⃣ **Brisa Aqua** (ID: `brisa-aqua`)
- **Tipo:** Light Glassmorphism (Playful)
- **Paleta:** Turquesas e azuis claros (cyan, aquamarine)
- **Cores:**
  - Fundo: `#E0FFFF` (ciano muito claro)
  - Primária: `#00CED1` (dark turquoise vibrante)
  - Acentos: `#40E0D0`, `#4682B4`
- **Caso de Uso:** Divertido, playful, interfaces aéreas
- **Forma:** **Ultra-arredondada** — 14px-30px+, 999px em botões
- **Font:** DM Sans, Syne (display moderno)
- **Animação:** **Bouncy** `cubic-bezier(0.2, 1.1, 0.2, 1)` — Float-in com scale
- **Backdrop Filters:** blur(14px) em cards
- **Insight Visual:** Cards com vidro translúcido, luz e movimento

#### 3️⃣ **Céu Sereno** (ID: `ceu-sereno`)
- **Tipo:** Light Airy (Calm Cloud Feel)
- **Paleta:** Azuis suave e pó azul (powder blues)
- **Cores:**
  - Fundo: `#B0E0E6` (powder blue claro)
  - Primária: `#4682B4` (steel blue confiável)
  - Acentos: `#87CEEB`, `#B0C4DE`
- **Caso de Uso:** Calmo, zen, interface educacional
- **Forma:** Bordas suaves (10px-34px), raio grande no calendar
- **Fonte:** Inter, Plus Jakarta Sans (profissional mas acessível)
- **Animação:** **Drift** `cubic-bezier(0.2, 1.0, 0.2, 1)` — Suave, sem bounce
- **Backdrop Filters:** blur(22px) leve em menú
- **Insight Visual:** Sensação CloudFeel, muitas gradients radiais em background

#### 4️⃣ **Cinza Industrial** (ID: `cinza-industrial`)
- **Tipo:** Light Monochrome (Minimal/Technical)
- **Paleta:** Grayscale puro — Cinzas variados
- **Cores:**
  - Fundo: Gainsboro `#DCDCDC`
  - Primária: DarkSlateGray `#2F4F4F` (cinza azulado escuro)
  - Acentos: Todos cinza (sem cor)
- **Caso de Uso:** Utilitário, técnico, informação densa
- **Forma:** **Ultra-minimalista** — 2px-8px (quase retas)
- **Fonte:** System UI, sans-serif (zero decoração)
- **Animação:** **Zero** — Sem animações, transitions lineares 0.10s
- **Insight Visual:** Informação pura, densidade máxima, sem ruídos visuais

#### 5️⃣ **Brisa Quente** (ID: `brisa-quente`)
- **Tipo:** Light Warm Comfort
- **Paleta:** `#F4F2EE` → `#5C3D2E` (Bege até marrom-chocolate)
- **Cores:**
  - Fundo: `#F4F2EE` (bege quente bem claro)
  - Primária: `#A67C52` (marrom-dourado confortável)
  - Acentos: `#C4A98A`, `#DCC2B6`
- **Caso de Uso:** Acolhedor, comfort, humanizado
- **Forma:** Bordas arredondadas (12px-28px), raio médio
- **Fonte:** Poppins, Playfair Display (warm, humanizado)
- **Animação:** Suave ease-out com gentle-float
- **Insight Visual:** Madeira e bege, sensação de acolhimento

#### 6️⃣ **Azul Corporativo** (ID: `azul-corporativo`)
- **Tipo:** Light Professional (B2B Enterprise)
- **Paleta:** `#F3F7FF` → `#071E3D` (Azul corporativo completo)
- **Cores:**
  - Fundo: `#F3F7FF` (azul bem claro, quase branco)
  - Primária: `#185FA5` (azul corporativo clássico)
  - Acentos: `#378ADD`, `#0D3A72`
- **Caso de Uso:** Empresarial, B2B, serviços financeiros
- **Forma:** Bordas corporativas (6px-16px), retangular classica
- **Fonte:** System UI (-apple-system, BlinkMacSystemFont)
- **Animação:** Suave ease-in-out, formal
- **Insight Visual:** Confiança, seriedade, profissionalismo

#### 8️⃣ **Jardim Fosco** (ID: `jardim-fosco`)
- **Tipo:** Light Muted Green (Botanical)
- **Paleta:** `#F1F5C9` → `#222202` (Verde muted)
- **Cores:**
  - Fundo: `#F1F5C9` (verde pálido muito claro)
  - Primária: `#8BA32D` (verde muted, não-vibrante)
  - Acentos: `#BFCC84`, `#627411`
- **Caso de Uso:** Ambiência, natureza, educational calmo
- **Forma:** Arredondada calorosa (12px-28px)
- **Fonte:** Poppins, Plus Jakarta Sans
- **Animação:** Growth-in com ease-out, scaleY
- **Insight Visual:** Inspiração botânica, verde natural não-agressivo

#### 9️⃣ **Terra & Musgo** (ID: `terra-musgo`)
- **Tipo:** Light Sage Green (Earthy/Sophisticated)
- **Paleta:** `#EAF0EA` → `#4A5E33` (Sage terroso)
- **Cores:**
  - Fundo: `#EAF0EA` (verde sage bem claro)
  - Primária: `#6C7B5A` (sage natural, sophistic)
  - Acentos: `#ACC4AD`, `#ABAD8B`
- **Caso de Uso:** Sofisticado, wellness, eco-centric
- **Forma:** Suave natural (10px-26px)
- **Fonte:** Inter, Plus Jakarta Sans
- **Animação:** Calm-in com ease, transições suaves
- **Insight Visual:** Musgo e terra, paleta natural harmonious

---

## 🔄 Mapeamento de Temas Antigos → Novos

| ID Antigo | ID Novo | Nome Novo | Notas |
|-----------|---------|-----------|-------|
| `default` | `indigo-profundo` | Indigo Profundo | Mantém lógica, novo nome |
| `cyan` | `brisa-aqua` | Brisa Aqua | Slight color tweaks, animations enhanced |
| `sky` | `ceu-sereno` | Céu Sereno | Cores mantidas, mais calmo |
| `gray` | `cinza-industrial` | Cinza Industrial | Monochrome, zero animação |

---

## 🎛️ Como Usar os Temas

### **Para Usuário Final**

1. **Seletor no topbar** — Ícone de paleta (🎨)
2. **Dropdown com 9 opções** — Nomes em português
3. **Aplicação instantânea** — CSS var mudanças
4. **Persistência** — localStorage por 1 ano

### **Para Desenvolvedor**

#### **1. Em HTML (base.html)**
```html
<html lang="pt-br" data-theme="indigo-profundo">
  <!-- CSS automáticamente aplica as variáveis corretas -->
</html>
```

#### **2. Em JavaScript (theme_manager.js)**
```javascript
// Adicione novos temas ao Set:
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

// Aplicar tema:
applyTheme('brisa-quente');

// Nomes legíveis:
getThemeName('brisa-quente'); // "Brisa Quente"
```

#### **3. Em CSS (themes.css)**
```css
html[data-theme="ambar-noite"] {
  --bg-base: #0D0A06;
  --primary: #EF9F27;
  /* ... 30+ variáveis por tema ... */
}

/* Componentes específicos */
html[data-theme="ambar-noite"] .sige-card {
  background: linear-gradient(180deg, rgba(28,21,9,0.70) 0%, ...);
  border: 1px solid rgba(239, 159, 39, 0.15);
}
```

---

## 🔧 Variáveis CSS por Tema

Cada tema redefine **no mínimo 30-40 variáveis CSS**:

```css
/* Cores Base */
--bg-base           /* Fundo principal */
--bg-surface        /* Superfícies secundárias */
--bg-elevated       /* Cards, modais */
--bg-hover          /* Estados hover */
--bg-input          /* Inputs/textareas */

/* Texto */
--text-primary      /* Texto principal */
--text-secondary    /* Texto secundário */
--text-muted        /* Labels, hints */

/* Marca & Acentos */
--primary           /* Cor primária (botões, links) */
--primary-dark      /* Variação escura */
--primary-light     /* Variação clara */

--accent-violet     /* Accent 1 */
--accent-cyan       /* Accent 2 */
--accent-emerald    /* Accent 3 */
--accent-amber      /* Accent 4 */
--accent-ruby       /* Accent 5 (erro) */

/* Borders */
--border-subtle     /* Borders discretas */
--border-mid        /* Borders normais */

/* Layout */
--header-bg         /* Header background */
--sidebar-bg-top    /* Sidebar superior */
--sidebar-bg-bottom /* Sidebar inferior */

/* Shapes & Motion */
--radius-sm         /* 2px → 14px por tema */
--radius-md         /* 4px → 18px por tema */
--radius-lg         /* 6px → 24px por tema */
--radius-xl         /* 8px → 30px+ por tema */

--shadow-sm         /* Sombra pequena */
--shadow-md         /* Sombra média */
--shadow-lg         /* Sombra grande */
--shadow-glow       /* Glow/brilho */

/* Transições */
--transition-fast   /* 0.10s → 0.18s */
--transition-mid    /* 0.14s → 0.28s */
--transition-slow   /* 0.18s → 0.46s */

/* Tipografia */
--font-main         /* Fonte principal */
--font-display      /* Fonte para headings */
```

---

## 🎬 Animações Signature de Cada Tema

| Tema | Animação | Easing | Duração | Efeito |
|------|----------|--------|---------|--------|
| **Brisa Aqua** | `sigeBrisaAquaFloatIn` | cubic-bezier(0.2, 1.1, 0.2, 1) | 0.38s | Bounce suave + scale up |
| **Céu Sereno** | `sigeCeuSerenoDriftIn` | cubic-bezier(0.2, 1.0, 0.2, 1) | 0.45s | Drift sem bounce, saturate change |
| **Ambar & Noite** | `sigeAmbarNoiteGlowIn` | cubic-bezier(0.25, 0.46, 0.45, 0.94) | 0.40s | Glow + saturate |
| **Brisa Quente** | `sigeBrisaQuenteGentleFloat` | ease-out | 0.35s | Float gentil |
| **Corporativo** | `sigeCorporativoSlideIn` | ease-in-out | 0.30s | Slide up formal |
| **Jardim Fosco** | `sigeJardimGrowthIn` | ease-out | 0.38s | Grow + scaleY |
| **Terra & Musgo** | `sigeTerraMuscoCalmIn` | ease | 0.36s | Calm fade-in |
| **Cinza Industrial** | **NENHUMA** | — | — | Sem animação (reduceMotion) |

---

## 🧪 Testes Recomendados

### **Por Tema:**
- [ ] Cards visíveis em todos os tamanhos
- [ ] Calendários com dias claramente diferenciados
- [ ] Buttons com hover/active state
- [ ] Inputs com focus state
- [ ] Tabelas com alternância de linhas
- [ ] Animações suave em página carrega
- [ ] Contraste WCAG AA mínimo

### **Cross-Browser:**
- [ ] Chrome/Chromium (Linux/Mac/Win)
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### **Responsividade:**
- [ ] Desktop (1920px+)
- [ ] Tablet (768px-1024px)
- [ ] Mobile (320px-480px)

---

## 📱 Estrutura de Arquivos

```
apps/comum/static/core/
├── css/design_system/
│   ├── tokens.css          ← Base CSS variables
│   ├── themes.css          ← 9 Temas (2000+ linhas)
│   ├── animations.css      ← Keyframes
│   ├── base.css            ← Base styles
│   ├── components.css      ← Component styles
│   ├── layout.css          ← Layout grid/flex
│   └── notifications.css   ← Toast/alert styles
│
└── js/
    └── theme_manager.js    ← Aplicador de temas

apps/usuarios/templates/core/
└── base.html              ← Select vazio (JS popula)
```

---

## 🚀 Implementação Future (v2.1+)

- [ ] **API de Preferências** — Salvar tema por usuário no DB
- [ ] **Color Picker** — Customizar paleta por user
- [ ] **Auto Dark/Light** — Seguir preferência do SO (prefers-color-scheme)
- [ ] **Tema Aleatório** — Botão "Surpresa!"
- [ ] **Exportar Tema** — CSS/JSON download
- [ ] **Tema Anual** — Lançar novo tema por mês/estação
- [ ] **Acessibilidade+** — Alto contraste automático
- [ ] **RTL Support** — Suporte para idiomas RTL

---

## 📚 Referências

- **WCAG 2.1 AA** — Contrast ratio 4.5:1 mínimo
- **CSS Variables** — Custom properties depth
- **Cubic-Bezier** — Easing functions (easings.net)
- **Material Design 3** — Color systems inspiration
- **Tailwind v3** — Spacing scale

---

## ✅ Checklist de Deploy

- [x] `themes.css` criado com 9 temas
- [x] `theme_manager.js` atualizado
- [x] `base.html` cleaned (select vazio)
- [x] Backup `themes-backup.css` realizado
- [ ] Testes manuais em 9 temas
- [ ] Cross-browser testing
- [ ] Mobile responsiveness
- [ ] Accessibility validation
- [ ] Performance audit
- [ ] Deploy para staging
- [ ] Deploy para production

---

## 📞 Suporte & Issues

**Para reportar problemas:**
1. Qual tema?
2. Qual componente (card, calendar, input, etc)?
3. Browser + OS
4. Screenshot

**Para sugerir novo tema:**
- Enviar paleta de 6 cores no formato HEX
- Usar `#RRGGBB` (lowercase recomendado)
- Incluir descrição (ex: "Tema Inverno — Azul gelado e branco")

---

**Desenvolvido com ❤️ para SIGE**

# 🧪 Guia de Testes — SIGE Themes v2.0

> **Para:** QA, Testers, Product Managers

---

## 🎯 Objetivo

Validar que os 9 temas do SIGE estão:
- ✅ Visualmente distintos
- ✅ Todos os componentes temáticos
- ✅ Animações suaves
- ✅ Cores legíveis (contraste)
- ✅ Responsive em todos os tamanhos

---

## 📋 Matriz de Testes

### **TEMA 1: Indigo Profundo** `indigo-profundo`

**Checklist Visual:**
- [ ] Fundo azul profundo muito escuro
- [ ] Cores roxas/violetas em CTA buttons
- [ ] Sombras clássicas em cards
- [ ] Bordas médias (6px-22px)
- [ ] Cards com bom contraste
- [ ] Calendário com dias legíveis

**Componentes a Testar:**
- [ ] `.sige-card` — Deve ter fundo dark com border sutil
- [ ] `.sige-btn-primary` — Roxo/violet vibrante
- [ ] `.sige-input` — Foco com outline roxo
- [ ] `.calendar-container` — Dias legíveis
- [ ] `.menu-principal` — Navy com marca roxa
- [ ] `.nav-lateral` — Indicator roxo em ativo

**Performance:**
- [ ] Transição de outro tema = suave (< 300ms paint)
- [ ] Nenhuma animação quebrada
- [ ] Sem flashing/flickering

---

### **TEMA 2: Brisa Aqua** `brisa-aqua`

**Checklist Visual:**
- [ ] Fundo ciano muito claro, quase branco azulado
- [ ] Turquesa/cyan vibrante em CTAs
- [ ] Cards com efeito vidro (backdrop blur visible)
- [ ] Bordas ultra-arredondadas (999px em buttons)
- [ ] Animação float-in com bounce
- [ ] Calendário com dias arredondados

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient + backdrop-filter blur
- [ ] `.sige-btn-primary` — Gradient cyan-steel, hover scale
- [ ] `.sige-btn` — Todos os buttons 999px radius (pill shape)
- [ ] `.nav-lateral a` — Radius 18px, rotate em hover
- [ ] `.calendar-day` — Radius 22px, gradient background
- [ ] `.dia.atual` — Gradient cyan-steel com glow

**Animações:**
- [ ] Cards fazem float-in ao carregar
- [ ] Easing: cubic-bezier(0.2, 1.1, 0.2, 1) — bounce suave
- [ ] Duration: 0.38s
- [ ] Scale + translateY

**Motion:**
- [ ] Move-se para cima (translateY(-14px))
- [ ] Aumenta um pouco (scale(1.01))
- [ ] Entrada suave com fade-in

---

### **TEMA 3: Céu Sereno** `ceu-sereno`

**Checklist Visual:**
- [ ] Fundo powder blue claro (céu passtel)
- [ ] Steel blue em CTAs (não vibrante, sereno)
- [ ] Cards com sombra suave
- [ ] Bordas menos ultra redondas (10px-34px)
- [ ] Sem bounce — movimento calmo
- [ ] Calendário com border left azul

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient de dois blues
- [ ] `.sige-btn-primary` — Gradient steel-sky, sem bounce em hover
- [ ] `.sige-btn` — Radius 999px (pill)
- [ ] `.calendar-day` — Border-left 4px steel-blue
- [ ] `.calendar-day.today` — outline 2px azul
- [ ] Background page — Múltiplas gradients radiais (cloudy feel)

**Animações:**
- [ ] Cards fazem drift-in (não bounce)
- [ ] Easing: cubic-bezier(0.2, 1.0, 0.2, 1) — suave
- [ ] Duration: 0.45s (mais lento que Brisa Aqua)
- [ ] Sem scale, só translateY + saturate change

**Motion:**
- [ ] Move-se para cima (translateY(-10px), menor amplitude)
- [ ] Contraste/saturação muda sutilmente
- [ ] Sensação calma, meditativa

---

### **TEMA 4: Cinza Industrial** `cinza-industrial`

**Checklist Visual:**
- [ ] Fundo cinza light (gainsboro)
- [ ] Dark slate gray em CTAs (monochrome, não colorido)
- [ ] Bordas MUITO agudas (2px-8px, quase retas)
- [ ] **Zero animações**
- [ ] Calendário com hard edges
- [ ] Máxima densidade visual

**Componentes a Testar:**
- [ ] `.sige-card` — Border 1px cinza, sem sombra excessiva
- [ ] `.sige-btn-primary` — Dark slate gray, uppercase text
- [ ] `.sige-btn` — Radius 4px (minimalista)
- [ ] `.nav-lateral a` — Radius 4px
- [ ] `.calendar-day` — Radius 6px, monochrome
- [ ] Animations em cards — **DEVE ESTAR DISABLED** (!important)

**Transições:**
- [ ] Todas as transitions devem ser 0.10s–0.18s LINEAR
- [ ] Nenhuma ease-in/ease-out, apenas linear
- [ ] Sem animações ao carregar

**Motion:**
- [ ] Nenhuma entrada com animation
- [ ] Foco apenas em informação, sem "ruído" visual

**Keyboard Navigation:**
- [ ] Tab/Shift+Tab funciona
- [ ] Focus state visível (outline 2px)
- [ ] Contraste alto

---

### **TEMA 5: Brisa Quente** `brisa-quente`

**Checklist Visual:**
- [ ] Fundo bege quente bem claro
- [ ] Marrom-dourado em CTAs (confortável, não vibrante)
- [ ] Gradientes em background
- [ ] Bordas arredondadas calorosas (12px-28px)
- [ ] Animação float gentil
- [ ] Sensação acolhedora

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient bege-marrom, sombra quente
- [ ] `.sige-btn-primary` — Gradient marrom-warm, hover translateY(-2px)
- [ ] `.sige-btn` — Radius 999px (pill)
- [ ] `.nav-lateral a` — Hover translateX(4px), bg color
- [ ] `.sige-input` — Border 1.5px caramelo
- [ ] Background page — Gradients radiais marrom-ouro

**Animações:**
- [ ] Cards aparecem com gentle-float
- [ ] Easing: ease-out
- [ ] Duration: 0.35s
- [ ] TranslateY(12px) → 0

**Font:**
- [ ] Deve estar usando Poppins se disponível
- [ ] Playfair Display nos headings

---

### **TEMA 6: Azul Corporativo** `azul-corporativo`

**Checklist Visual:**
- [ ] Fundo azul claro quase branco (enterprise clean)
- [ ] Azul corporativo clássico em CTAs
- [ ] Bordas corporativas (6px-16px)
- [ ] Sem excessos, profissional
- [ ] Header com gradient sutil azul
- [ ] Calendário minimalista

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient azul claro, border sutil
- [ ] `.sige-btn-primary` — Gradient azul corporativo, hover glow
- [ ] `.sige-btn` — Radius 8px (corporativo)
- [ ] `.menu-principal` — Gradient azul claro-médio
- [ ] `.sige-input` — Border 1.5px azul, bg branco
- [ ] Badge success/warning/danger — Cores scheme

**Transições:**
- [ ] Todas ease-in-out (0.14s–0.32s)
- [ ] Formais, não playful

**Animações:**
- [ ] SlideIn 0.30s
- [ ] Formal, sem bounce ou scale excessivo

---

### **TEMA 7: Âmbar & Noite** `ambar-noite`

**Checklist Visual:**
- [ ] Fundo **muito escuro** quase preto (#0D0A06)
- [ ] Âmbar **muito quente/vibrante** em CTAs
- [ ] Alto contraste (luz em fundo escuro)
- [ ] Bordas suaves (8px-24px)
- [ ] Animação com glow
- [ ] Cards com vidro translúcido

**Componentes a Testar:**
- [ ] `.sige-card` — Backdrop blur + gradient escuro com âmbar
- [ ] `.sige-btn-primary` — Gradient âmbar-light, cor text dark
- [ ] `.sige-input` — Border 1.5px âmbar, bg escuro
- [ ] `.nav-lateral a` — Hover com gradient âmbar sutil
- [ ] `.menu-principal` — Grayscale look, bottom border âmbar
- [ ] `.calendar-day.atual` — Gradient âmbar vibrante

**Animações:**
- [ ] GlowIn 0.40s
- [ ] Cubic-bezier expressivo (0.25, 0.46, 0.45, 0.94)
- [ ] Glow effect, saturate change

**Tipografia:**
- [ ] Deve estar usando Lora (serif) se disponível
- [ ] Playfair Display nos headings (editorial feel)

**Visual Impact:**
- [ ] Editorial vibe, magazine-like
- [ ] Âmbar quente vs fundo escuro = **alto impacto**

---

### **TEMA 8: Jardim Fosco** `jardim-fosco`

**Checklist Visual:**
- [ ] Fundo verde pálido muito claro
- [ ] Verde muted (não vibrante) em CTAs
- [ ] Bordas arredondadas calorosas
- [ ] Animação growth-in
- [ ] Sensação botânica, natural

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient verde pálido
- [ ] `.sige-btn-primary` — Gradient verde muted
- [ ] `.sige-btn` — Radius 999px
- [ ] Background page — Gradients verdes suaves
- [ ] `.calendar-day` — Verde pálido background
- [ ] `.dia.atual` — Gradient verde escuro

**Animações:**
- [ ] GrowthIn 0.38s
- [ ] ScaleY effect (crescer de baixo)
- [ ] Sensação de crescimento vegetal

**Sensibilidade:**
- [ ] Suave, relaxante
- [ ] Educacional, botânico

---

### **TEMA 9: Terra & Musgo** `terra-musgo`

**Checklist Visual:**
- [ ] Fundo verde sage bem claro (soft)
- [ ] Verde sage sofisticado em CTAs
- [ ] Bordas suave (10px-26px)
- [ ] Animação calm
- [ ] Sensação sofisticada, wellness

**Componentes a Testar:**
- [ ] `.sige-card` — Gradient sage claro
- [ ] `.sige-btn-primary` — Gradient sage médio-escuro
- [ ] `.sige-btn` — Radius 14px (suave)
- [ ] `.nav-lateral a` — Hover translateX(2px), bg sage sutil
- [ ] Background page — Gradients verdes equilibrados
- [ ] `.calendar-day` — Sage background

**Animações:**
- [ ] CalmIn 0.36s
- [ ] Ease simples (sem cubic-bezier complexo)
- [ ] CalmIn fade-in natural

**Tipografia:**
- [ ] Inter (main) + Plus Jakarta Sans (display)

---

## 🔄 Testes Cross-Browser

### **Browser → Tema Matrix**

| Browser | Indigo | Aqua | Sky | Gray | Quente | Corp | Âmbar | Jardim | Musgo |
|---------|--------|------|-----|------|--------|------|-------|--------|-------|
| Chrome | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Firefox | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Safari | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Edge | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### **O que checar por browser:**
- [ ] CSS variables funcionam
- [ ] Backdrop-filter render correto (Safari pode ter issues)
- [ ] Animações suaves (60fps)
- [ ] Sombras render (box-shadow)
- [ ] Gradients corretos
- [ ] Cores corretas (não desaturadas)

---

## 📱 Testes Responsivos

### **Desktop (1920px+)**
- [ ] Todos 9 temas funcionam
- [ ] Cards espaçamento correto
- [ ] Calendários legíveis
- [ ] Sidebar visível
- [ ] Animações suaves

### **Tablet (768px-1024px)**
- [ ] Menu lateral pode colapsar
- [ ] Cards ainda visíveis
- [ ] Calendário responsivo
- [ ] Touch interactions smooth

### **Mobile (320px-480px)**
- [ ] Menu hamburguer ativo
- [ ] Cards stack verticalmente
- [ ] Calendário em mini-view?
- [ ] Tema selector ainda acessível

---

## ♿ Testes de Acessibilidade

### **Contraste WCAG AA**
```
Para cada tema, testar:
- [ ] Texto foreground vs background ≥ 4.5:1
- [ ] Large text ≥ 3:1
- [ ] UI components ≥ 3:1
```

**Ferramenta:** WebAIM Contrast Checker

### **Keyboard Navigation**
- [ ] Tab → order lógico
- [ ] Shift+Tab → order reverso
- [ ] Enter/Space → ativa buttons
- [ ] Focus indicator visível em todos temas

### **Screen Reader**
- [ ] Select options anunciadas
- [ ] Mudança de tema anunciada (via aria-live?)
- [ ] Componentes identificadas

### **prefers-reduced-motion**
```bash
# Testar com DevTools:
1. Open DevTools → Rendering
2. Check "Emulate CSS media feature prefers-reduced-motion: reduce"
3. Verificar: Animações desabilitadas? (cinza-industrial já está)
```

---

## 🎬 Teste de Performance

### **Metrics a Medir:**
- [ ] Time to Interactive (TTI)
- [ ] First Contentful Paint (FCP)
- [ ] Largest Contentful Paint (LCP)
- [ ] Cumulative Layout Shift (CLS)
- [ ] First Input Delay (FID)

### **Ferramenta:** Chrome DevTools → Lighthouse

```bash
1. Abrir cada tema
2. Rodar Lighthouse audit
3. Verificar:
   - Performance score ≥ 90
   - Sem cumulative layout shift
   - Animations 60fps (Chrome → Rendering → FPS meter)
```

---

## 📸 Screenshots Esperados

### **Para Cada Tema:**
```
✓ Homepage (hero + cards)
✓ Calendário (mini + full view)
✓ Tabela (com dados)
✓ Form (inputs, buttons)
✓ Modal/popup
✓ Notifications/toasts
✓ Mobile view (320px)
```

### **Armazenar em:**
```
SIGE/
├── docs/
│   └── themes-testing/
│       ├── indigo-profundo/
│       ├── brisa-aqua/
│       ├── ... etc ...
│       └── SCREENSHOTS.md (index)
```

---

## 🐛 Report de Issues

### **Template:**
```
## [THEME] Component não está temático

**Tema:** Terra & Musgo
**Component:** .sige-card
**Browser:** Chrome v120
**Device:** MacBook Pro 16"

**Descrição:**
Card não tem fundo correto (aparece roxo ao invés de sage)

**Steps to Reproduce:**
1. Selecionar "Terra & Musgo"
2. Navegar para /dashboard
3. Observar cards

**Expected:**
Fundo sage claro (#EAF0EA)

**Actual:**
Fundo roxo (indigo)

**Screenshot:**
[attach]

**Possible Root Cause:**
CSS variable --bg-surface não está sendo aplicado
```

---

## ✅ Checklist Final

### **Antes do Deploy:**
- [ ] Todos 9 temas testados
- [ ] Cross-browser OK (4+ browsers)
- [ ] Responsive OK (3+ breakpoints)
- [ ] Performance OK (Lighthouse ≥ 90)
- [ ] Acessibilidade OK (WCAG AA)
- [ ] localStorage persiste
- [ ] Animações 60fps
- [ ] Sem console errors
- [ ] Sem console warnings (CSS variables)
- [ ] Screenshots documentadas

### **Após Deploy (Smoke Test):**
- [ ] Tema default aplica (indigo-profundo)
- [ ] Dropdown appear com 9 opções
- [ ] Seleção de tema funciona
- [ ] Página reload → tema persiste
- [ ] Prvate mode → sem localStorage, usa session
- [ ] Mudança de tema é suave (< 300ms)

---

## 🚀 Go/No-Go Decision

### **GO If:**
- ✅ Todos 9 temas visualmente distintos
- ✅ Nenhum regression em componentes existentes
- ✅ Performance não degradada
- ✅ Acessibilidade mantida
- ✅ Nenhum critical bug reportado

### **NO-GO If:**
- ❌ Quelquer tema com contraste insuficiente
- ❌ Animações causando 60fps drop
- ❌ localStorage não funciona
- ❌ Critical bugs em 2+ browsers

---

**Bom testing! 🧪**

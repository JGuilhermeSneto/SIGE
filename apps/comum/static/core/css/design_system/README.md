# 🎨 Premium Design System — SIGE

O diretório que define a **Identidade Visual Absoluta** do SIGE. Centraliza tokens de cores, tipografia, bordas, animações e temas para garantir consistência em 100% das telas.

## 🌈 Sistema de Temas

O SIGE possui **9 temas completos**, aplicados via `<html data-theme="...">`:

| Tema | Slug | Característica |
|---|---|---|
| Índigo Profundo | `indigo-profundo` | Dark mode neon, bordas violeta |
| Brisa Aqua | `brisa-aqua` | Aquático, glassmorphism |
| Céu Sereno | `ceu-sereno` | Sky gradient, azul sereno |
| Cinza Industrial | `cinza-industrial` | Brutalista, bordas demarcadas em todos os cards |
| Azul Corporativo | `azul-corporativo` | Corporativo, bordas azuis em todos os cards |

## 🃏 Bordas de Cards (Atualização Recente)

Os temas **Azul Corporativo** e **Cinza Industrial** receberam bordas de cor visíveis em **todos os tipos de card** do sistema:

```css
/* Seletores cobertos (por tema) */
.sige-card, .sige-glass-card, .card, .card-tabela,
.card-listagem, .card-turma, .card-disciplina,
.card-stats, .stat-card, .bi-card, .metric-card,
.login-card, .perfil-card, .calendar-container,
.form-container, .msg-list li ...
```

- **Azul Corporativo**: `2px solid rgba(21, 101, 192, 0.45)` — hover: `0.80`.
- **Cinza Industrial**: `2px solid` cinza-ardósia + `border-top: 3px` industrial.

## 🏗️ Filosofia de Tokens

Nenhuma cor bruta deve ser usada diretamente. Sempre use tokens:

```css
/* ❌ Errado */
background: #d11;

/* ✅ Correto */
background: var(--accent-ruby);
```

**Tokens principais:**
- `--primary`: Cor de ação principal do tema ativo.
- `--accent-ruby`: Alertas médicos e exclusões.
- `--accent-emerald`: Confirmações e status positivo.
- `--accent-amber`: Atenção e pendências.
- `--bg-surface`, `--bg-elevated`: Backgrounds de cards.
- `--border-subtle`, `--border-mid`, `--border-strong`: Bordas por intensidade.

## 🪄 Classes Globais de Botões

| Classe | Uso |
|---|---|
| `.sige-btn-primario` | Botão de ação principal (gradiente do tema) |
| `.btn-sige-secundario` | Botão de borda/outline |
| `.btn-sige-ruby` | Exclusão e alertas críticos |
| `.btn-filtro` | Filtros e seleção de abas |

> **Regra de ouro**: Nenhum `style=""` inline em novos templates. Novas classes devem ser criadas neste diretório.

*Atualizado em 27/04/2026 — Bordas universais em cards para Azul e Cinza.*

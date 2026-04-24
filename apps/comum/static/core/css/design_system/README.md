# 🎨 Premium BI Design System

O diretório responsável pela Identidade Visual Absoluta do SIGE. Este sistema centraliza a tipografia, a paleta de cores e o formato dos botões para garantir uma paridade de layout perfeita e uma UI/UX deslumbrante em todas as telas da plataforma.

## 🏗️ Filosofia "Azul Corporativo" e Glassmorphism

As últimas grandes atualizações implementaram a restauração do conceito **Azul Corporativo** clássico somado a visuais modernos que incluem:
1. **Transparência e Desfoque (Glassmorphism)**: Efeitos de fundo embaçado (`backdrop-filter`) em painéis flutuantes (como faturas e alergias do aluno).
2. **As Pílulas Perfeitas**: Todas as interfaces utilizam botões super-arredondados (`border-radius: 48px`), rompendo a arquitetura web agressiva clássica do bootstrap e fornecendo um design tátil de ponta.

## 🌈 Tokens Semânticos de Cores

O coração do design está nas variáveis (tokens) em `.root`. Nenhuma cor bruta (`#FF0000`) deve ser digitada diretamente dentro do CSS ou HTML. O desenvolvedor deve sempre usar os Tokens CSS:

```css
/* Errado */
background-color: #d11;

/* Correto */
background-color: var(--accent-ruby);
```

- `--accent-ruby`: Vermelhos para Destaques Médicos e Alertas Críticos.
- `--accent-emerald`: Verdes para faturas Pagas e links seguros.
- `--accent-blue`: Ações primárias de navegação.
- `--surface-overlay`: Backgrounds de painéis Glass.

## 🪄 Classes Utilitárias (Botões Globais)

Para evitar botões diferentes em páginas diferentes, usamos as classes declaradas globais no Design System:

- `.btn-premium-primary`: O clássico botão preenchido vibrante.
- `.btn-premium-outline`: Botão transparente apenas com as bordas em alto contraste.
- `.btn-premium-ruby`: Variável para exclusão ou alertas críticos.

O SIGE proíbe o uso de estilos *inline* (como `style="background: blue; border-radius: 10px;"`) em novos templates. Qualquer nova classe deve ser referenciada ou criada neste diretório.

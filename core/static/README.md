# SIGE · Static Assets

Contém os arquivos estáticos (CSS, Javascript, Imagens) que alimentam a interface do sistema.

## Estrutura de Diretórios

- **`core/css/`**: Folhas de estilo divididas por módulo.
- **`core/css/design_system/`**: **Coração visual do projeto.** Contém o `tokens.css` com as variáveis HSL de cores, fontes e espaçamentos.
- **`core/js/`**: Lógica de interface, manipulação de DOM e requisições AJAX (ex: `registration_wizard.js`).
- **`core/img/`**: Logos, ícones e ilustrações do sistema.

## Sistema de Design (Premium)

O projeto migrou para um modelo de "Design Premium". Todas as novas interfaces devem utilizar:
- **Fontes**: Syne (para títulos impactantes) e DM Sans (para leitura confortável).
- **Cores**: Variáveis HSL definidas em `tokens.css`.
- **Efeitos**: Glassmorphism e micro-animações definidas globalmente.

## Manutenção

Ao criar um novo estilo CSS, sempre importe os tokens primeiro ou utilize as variáveis globais que já estão disponíveis no `base.html`.

# 🔧 App: Comum

App utilitária compartilhada por todos os módulos do SIGE. Não possui views próprias.

## Responsabilidades
- **Design System**: CSS global (`gestao_painel.css`, `infraestrutura.css`, variáveis de tema)
- **Template Tags**: `custom_tags`, `get_item`, `vite_assets`
- **Utilitários**: helpers de rede (`get_client_ip`), formatação de dados
- **Middlewares**: `TenantMiddleware` para suporte a multi-tenancy
- **Static Files**: centralização de todos os assets CSS/JS/Fonts

## Estrutura Importante
```
comum/
├── static/core/css/    # Design System tokens e componentes
├── templatetags/       # Tags e filtros personalizados do Django
├── middleware/         # Middlewares compartilhados
└── utils/              # Funções auxiliares reutilizáveis
```

> Este app é o coração do Design System. Qualquer novo componente visual deve ser adicionado aqui.

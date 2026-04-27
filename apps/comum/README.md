# 🧱 Módulo Comum & Infraestrutura Base

Este é o alicerce técnico do SIGE, fornecendo as bases para o isolamento de dados, segurança avançada e a identidade visual do sistema.

## 🏢 Fundação Multi-Tenancy
O SIGE é arquitetado para suportar múltiplas instituições de forma isolada:
- **TenantModel**: Modelo base que injeta o vínculo com a `Instituicao` em todo o ecossistema.
- **TenantMiddleware**: Garante que o usuário veja apenas os dados da sua instituição, resolvendo o escopo via thread-local.

## 🎨 Design System Premium
Localizado em `static/core/`, este sistema define a estética "Premium Glassmorphism" do projeto:
- **Tokens CSS**: Gerenciamento de cores, espaçamentos e arredondamentos (48px).
- **Temas Dinâmicos**: Suporte a temas Azul Corporativo, Dark Mode e variações industriais.
- **Micro-animações**: Feedback visual fluido para uma experiência de usuário superior.

## 🔒 Segurança & Auditoria
- **Campos Criptografados**: Suporte nativo a `EncryptedCharField` e `EncryptedDateField`.
- **Middleware de Auditoria**: Registro de trilha de acesso em conformidade com a **LGPD**.
- **Validadores**: Lógica centralizada para CPF, CNPJ e outros documentos.

> Atualizado em 27/04/2026 — Núcleo de Design System e Multi-Tenancy consolidado.

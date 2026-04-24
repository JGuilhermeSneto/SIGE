# Módulo Comum

## Visão geral

O app `apps.comum` fornece recursos compartilhados entre os apps do SIGE, incluindo formulários base, templatetags, utilitários e arquivos estáticos globais.

## Funcionalidades principais

- Formulários base para validação e estilo comuns.
- **Validação de Documentos**: Utilitários para validação matemática de CPF e CNPJ reais via `validators.py`.
- **Criptografia de Campos**: Implementação de `EncryptedCharField`, `EncryptedDateField` e outros campos protegidos em `utils/fields.py`.
- **Design System & Segurança**: Tokens de design e cabeçalhos de segurança centralizados.

## Estrutura de pastas

- `forms/` — formulários compartilhados.
- `templatetags/` — tags Django customizadas.
- `utils/` — funções auxiliares reutilizáveis.
- `static/` — recursos estáticos globais.

## Uso principal

Use este app para centralizar componentes reutilizáveis e garantir consistência visual e comportamental entre os módulos.

## Observações

Este módulo reduz duplicação e facilita a manutenção de estilos e helpers entre apps.

> Atualizado em 2026-04-22.

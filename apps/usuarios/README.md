# 👥 App: Usuários

Módulo central de identidade, autenticação e perfis do SIGE.

## Responsabilidades
- Autenticação via **matrícula** (formato: `YYYYTTTUUUU`)
- Autenticação em Dois Fatores (2FA — TOTP)
- Gestão de perfis: Aluno, Professor, Gestor, Responsável, TI
- Controle de permissões e grupos (RBAC)
- Upload e gestão de foto de perfil (Cloudinary)
- Context processors para notificações globais

## Modelos Principais
- `auth.User` (Modelo padrão estendido via Perfis)
- `Gestor`, `Professor`, `Aluno`, `Responsavel` (Perfis OneToOne)

## Backends de Autenticação
- `MatriculaAuthBackend` — login principal por matrícula
- `AxesBackend` — proteção contra força bruta
- `ModelBackend` — fallback padrão do Django

## Permissões por Grupo
| Grupo | Acesso |
|---|---|
| `Gestor` | Visão global de todos os módulos |
| `Professor` | Acadêmico (próprias turmas) |
| `Aluno` | Próprias notas, frequência e documentos |
| `Responsável` | Dados dos dependentes vinculados |
| `TI — Operador` | Área de TI, segurança e chamados |
| `TI — Coordenação` | Operações avançadas e manutenção |

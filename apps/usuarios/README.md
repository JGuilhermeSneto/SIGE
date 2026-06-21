# 👥 App: Usuários (v2.3)

Módulo central de identidade, autenticação e perfis do SIGE. Integrado ao app SIGE Mobile via JWT.

![Testes](https://img.shields.io/badge/Testes-Estável-brightgreen?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~82%25-green?style=flat-square)

## Responsabilidades
- Autenticação via **matrícula** (formato: `YYYYTTTUUUU`) gerada automaticamente no `save()` do `Aluno`
- Autenticação em Dois Fatores (2FA — TOTP)
- Gestão de perfis: Aluno, Professor, Gestor, Responsável, TI
- Controle de permissões e grupos (RBAC)
- Upload e gestão de foto de perfil (Cloudinary + REST API para mobile)
- Context processors para notificações globais

## ⚠️ Comportamento Crítico — `Aluno.save()`
O método `save()` do modelo `Aluno` **sobrescreve automaticamente** o `user.username` com a matrícula gerada (`YYYYTTTUUUU`). Qualquer código de teste ou serviço que crie um `Aluno` deve usar `force_login(aluno.user)` em vez de `login(username=...)`, pois o username original é descartado.

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

## 📊 Cobertura de Testes

| Arquivo de Teste | Status |
|---|:---:|
| `test_paineis.py` | ✅ |
| `test_perfil_service.py` | ✅ |
| `test_perfis_utils.py` | ✅ |
| `test_registros.py` | ✅ |
| `test_usuarios_forms_autenticacao.py` | ✅ |
| `test_usuarios_forms_perfis.py` | ✅ |
| `test_views_autenticacao.py` | ✅ |
| `test_views_perfis.py` | ✅ |

## 📱 Integração Mobile (Junho 2026)
- **Foto de perfil via API**: `PUT /api/v1/aluno/perfil/` com `multipart/form-data` para upload direto do SIGE Mobile.
- **Consulta de perfil**: `GET /api/v1/aluno/perfil/` retorna dados do aluno incluindo `foto_url`.

---
> Atualizado em Junho de 2026 — Endpoints REST expostos para SIGE Mobile.

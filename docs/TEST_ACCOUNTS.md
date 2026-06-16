# Contas de Teste (Mobile)

Registra as contas criadas para testes do cliente mobile (login por matrícula + senha).

- **Turma usada:** id 16
- **Instituição:** id 1
- **Senha comum:** `SenhaSIGE2026`

## Alunos de Teste — Turma 16 (Contas Ativas ✅)

> Criados via `scripts/fix_test_alunos.py`. Verificados e funcionais no banco.

| Nome            | Matrícula   | Username    | Senha          | Ativo |
|-----------------|-------------|-------------|----------------|-------|
| Junior Teste    | 202677588   | 202677588   | SenhaSIGE2026  | ✅    |
| Israel Teste    | 202677589   | 202677589   | SenhaSIGE2026  | ✅    |
| Guilherme Teste | 202677590   | 202677590   | SenhaSIGE2026  | ✅    |
| Pedro Teste     | 202677591   | 202677591   | SenhaSIGE2026  | ✅    |

## Como usar no App Mobile

1. Abra o app SIGE Mobile (via Expo Go).
2. No campo **MATRÍCULA OU E-MAIL**, digite a matrícula (ex: `202677588`).
3. No campo **CHAVE DE ACESSO**, digite `SenhaSIGE2026`.
4. Clique em **CONECTAR**.
5. Você verá a mensagem **"Conexão Estabelecida"** e entrará no app.

## Observações

- Use a **matrícula** como identificador de login no app mobile.
- As senhas devem ser alteradas antes de subir para ambientes públicos.
- Para recriar/corrigir essas contas, execute: `python scripts/fix_test_alunos.py`

## Outras contas no banco (criadas anteriormente)

Existem outros alunos no banco com matrículas no padrão `2026{turma_id}{aluno_id}` (ex: `20260160184`).
Essas contas **não possuem senha configurada** — use apenas as contas da tabela acima para testes mobile.
# 🛡️ Política de Segurança — SIGE (Shield v1.2)

> **Atualizado:** Maio de 2026 | **Conformidade:** LGPD · OWASP Top 10

Este documento descreve todas as camadas de proteção implementadas no SIGE para garantir a integridade dos dados e a segurança dos usuários.

---

## 1. 🔐 Autenticação e Controle de Acesso

### Login por Matrícula
O SIGE utiliza matrícula institucional (formato `YYYYTTTUUUU`) como identificador primário, eliminando a dependência de e-mails genéricos.

### Autenticação em Dois Fatores (2FA — TOTP)
- Implementado via **Django Two-Factor Auth**.
- Compatível com Google Authenticator, Microsoft Authenticator e Authy.
- **Obrigatório** para contas com perfil de Gestor e Staff.
- Códigos de recuperação estáticos disponíveis para emergências.

### Proteção contra Força Bruta
- **Django Axes**: Bloqueio após **5 tentativas falhas** de login.
- Bloqueio por **1 hora** (configurável).
- Logs de tentativas registrados automaticamente.

---

## 2. 🍯 Honeypot e Detecção de Intrusão

### Admin Honeypot
Monitoramento de acessos não autenticados a caminhos sensíveis (`/admin/`):
- Após **3 tentativas**, o IP é banido automaticamente por **24 horas**.
- Registrado no painel de **Blacklist IP** (visível na Área de Segurança TI).

### Auto-Blacklist por Volume de Erros
- **Gatilho**: 10 erros em 60 segundos a partir do mesmo IP.
- **Ação**: Bloqueio preventivo por **1 hora**.
- Objetivo: Mitigar ataques de enumeração e DDoS primitivos.

---

## 3. 🧼 Proteção de Dados (LGPD)

### Sanitização de PII (PII Scrubbing)
Antes de gravar qualquer log de erro no banco, o middleware sanitiza automaticamente:
- CPFs (mascarados como `***.***.***-**`)
- Endereços de e-mail
- Telefones

### Criptografia de Dados Sensíveis
Campos de saúde, financeiro e documentos pessoais são armazenados com **criptografia AES/Fernet** em nível de campo (`django-encrypted-model-fields`).

### Auditoria LGPD (AuditMiddleware)
Todos os acessos às seguintes áreas são registrados no `LogAuditoria`:
- `/saude/`, `/financeiro/`, `/admin/`, `/seguranca/`, `/ti/`

---

## 4. 🛂 Validação e Upload Seguro

### Validação de Documentos Brasileiros
- **CPF e CNPJ**: Validação matemática com checksum (via `validate-docbr`).
- Impede cadastro de documentos gerados aleatoriamente ou inválidos.

### Força de Senha (ZXCVBN)
- Implementado via algoritmo **Dropbox ZXCVBN**.
- Senhas com score baixo são rejeitadas no cadastro e na alteração.

### Validação de Arquivos (Magic Numbers)
- O sistema lê o cabeçalho binário do arquivo para validar a assinatura real.
- Um script `.php` disfarçado de `.jpg` é detectado e bloqueado.

---

## 5. 🌐 Segurança de Comunicação (Produção)

| Proteção | Status |
|---|---|
| **HTTPS / SSL** | Gerenciado pelo Render (automático) |
| **HSTS** | Ativo por 1 ano em produção |
| **Secure Cookies** | `SESSION_COOKIE_SECURE=True` |
| **HttpOnly Cookies** | `SESSION_COOKIE_HTTPONLY=True` |
| **CSP** | `Content-Security-Policy` ativo |
| **CORS** | Restrito a origens confiáveis |

---

## 6. 🔬 Auditoria de Segurança (CI/CD)

O pipeline de CI executa automaticamente a cada commit:
- **Bandit**: Varredura de vulnerabilidades em código Python.
- **Pip-audit**: Verificação de CVEs em dependências do `requirements.txt`.
- **Django check --deploy**: Checklist nativo de segurança para produção.

---

> [!IMPORTANT]
> Qualquer alteração no `AuditMiddleware`, na lógica de criptografia ou nas políticas de autenticação deve ser revisada por um membro da equipe de TI antes do merge.

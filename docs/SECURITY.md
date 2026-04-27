# 🛡️ Política de Segurança — SIGE (Auditoria Jarvis)

Este documento descreve as camadas de proteção implementadas no SIGE para garantir a integridade dos dados e a segurança dos usuários, atualizado sob a auditoria **Jarvis 2026**.

---

## 1. Proteções Ativas

### 🚫 Proteção contra Força Bruta (Brute Force)
Utilizamos o **Django Axes** para monitorar tentativas de login.
- **Limite**: 5 tentativas falhas.
- **Bloqueio**: O IP ou usuário é bloqueado por **1 hora** após atingir o limite.

### 📜 Política de Segurança de Conteúdo (CSP)
Implementamos cabeçalhos **CSP** para mitigar ataques de **XSS** e injeção de dados.
- Bloqueio de scripts de fontes desconhecidas.
- Compatibilidade total com o workflow de desenvolvimento **Vite/React**.

### 🚥 Limitação de Taxa (API Throttling)
- **Anônimos**: 100 requisições/dia.
- **Usuários Autenticados**: 1000 requisições/dia.

---

## 2. Camadas Adicionais (Atualização de Segurança 27/04/2026)

### 🔐 Autenticação em Dois Fatores (2FA)
Implementamos o **Django Two-Factor Auth**.
- **TOTP**: Suporte para Google Authenticator, Microsoft Authenticator e Authy.
- **Enforcement**: Obrigatório para contas com permissões administrativas (Gestores e Staff).
- **Códigos de Recuperação**: Geração de códigos estáticos de uso único para emergências.

### 👁️ Monitoramento de Erros (Sentry)
Integração com **Sentry SDK** para detecção em tempo real de:
- Erros de runtime que podem indicar tentativas de exploração.
- Falhas em transações críticas (Saúde/Financeiro).
- Logs de segurança capturados via `sentry_sdk.init`.

### 📝 Auditoria LGPD (Audit Middleware)
Middleware customizado para logar acessos a áreas de dados sensíveis.
- **Áreas Auditadas**: Saúde, Financeiro, Documentos Oficiais.
- **Dados Capturados**: Username, Timestamp, Caminho da URL, IP de Origem.

---

## 2. Validação de Dados e Documentos

### 🪪 Validação de CPF/CNPJ (Real)
Diferente de versões anteriores que usavam apenas Regex, o SIGE agora implementa **validação matemática (checksum)** para documentos brasileiros via biblioteca `validate-docbr`.
- Impede o cadastro de CPFs gerados aleatoriamente ou inválidos.
- Aplicação automática em todos os perfis (Alunos, Professores, Gestores).

### 🔑 Força de Senha (ZXCVBN)
- **ZXCVBN**: Implementamos o algoritmo de estimativa de força de senha do Dropbox. 
- Senhas que não atingem o score de segurança mínimo são rejeitadas durante o cadastro ou alteração.

---

## 3. Segurança de Dados e Comunicação

### 🔐 Comunicação (Produção)
- **HSTS**: Ativado por 1 ano.
- **SSL Redirect**: Redirecionamento automático para HTTPS.
- **Secure Cookies**: Cookies marcados como `Secure` e `HttpOnly` (exceto CSRF para compatibilidade com o frontend).

---

## 4. Auditoria e CI/CD
O pipeline de CI executa:
- **Bandit**: Varredura de vulnerabilidades Python.
- **Pip-audit**: Verificação de dependências.
- **Check --deploy**: Verificação de segurança nativa do Django.

*Última atualização: Abril de 2026 — Auditoria Jarvis*

# 🛡️ Política de Segurança — SIGE (Auditoria Jarvis)

Este documento descreve as camadas de proteção implementadas no SIGE para garantir a integridade dos dados e a segurança dos usuários, atualizado sob a auditoria **Jarvis 2026**.

---

## 1. Proteções Ativas & Hardening (Shield v1.2)

### 🚫 Proteção contra Força Bruta (Brute Force)
Utilizamos o **Django Axes** e **Hardening Middleware** para monitorar tentativas de login.
- **Limite**: 5 tentativas falhas.
- **Bloqueio**: O IP ou usuário é bloqueado por **1 hora** após atingir o limite.

### 🍯 Admin Honeypot (Armadilha para Bots)
O sistema monitora tentativas de acesso não autenticadas a caminhos administrativos sensíveis como `/admin/`, `wp-admin/`, `phpmyadmin/`.
- **Ação**: Banimento automático do IP por **24 horas** após 3 tentativas de invasão detectadas.

### 🌑 Auto-Blacklist Inteligente
Monitoramento em tempo real do volume de erros gerados por um único IP.
- **Gatilho**: 10 erros críticos em 60 segundos.
- **Ação**: Bloqueio preventivo do IP por **1 hora** para mitigar ataques de enumeração ou DoS.

### 🧼 Sanitização de PII (PII Scrubbing)
Para conformidade estrita com a **LGPD**, o sistema implementa uma camada de "limpeza" de logs.
- **Lógica**: Antes de gravar qualquer log de erro no banco de dados (`LogErro`), CPFs e E-mails são mascarados via regex.
- **Garantia**: Desenvolvedores e gestores técnicos não têm acesso a dados pessoais via trilhas de erro.

### 🛡️ Validação de Assinatura (Magic Numbers)
Proteção contra ataques de upload (MIME-Type sniffing).
- **Lógica**: O sistema lê o cabeçalho binário do arquivo para validar se o conteúdo corresponde à extensão (Ex: Um script `.php` disfarçado de `.jpg` será bloqueado).

---

## 2. Camadas Adicionais (Atualização Shield 06/05/2026)

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
- **SSL Redirect**: Redirecionamento automático para HTTPS (Gerenciado pelo Render).
- **Banco de Dados Seguro**: Conexão com **MySQL (Aiven)** forçada via `ssl-mode=REQUIRED`, garantindo que nenhum dado trafegue sem criptografia entre o app e o banco.
- **Secure Cookies**: Cookies marcados como `Secure` e `HttpOnly` (exceto CSRF para compatibilidade com o frontend).

---

## 4. Auditoria e CI/CD
O pipeline de CI executa:
- **Bandit**: Varredura de vulnerabilidades Python.
- **Pip-audit**: Verificação de dependências.
- **Check --deploy**: Verificação de segurança nativa do Django.

*Última atualização: 28 de Abril de 2026 — Auditoria Jarvis (Cloud Production)*

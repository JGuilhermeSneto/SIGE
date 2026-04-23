# 🛡️ Política de Segurança — SIGE

Este documento descreve as camadas de proteção implementadas no SIGE para garantir a integridade dos dados e a segurança dos usuários.

---

## 1. Proteções Ativas

### 🚫 Proteção contra Força Bruta (Brute Force)
Utilizamos o **Django Axes** para monitorar tentativas de login.
- **Limite**: 5 tentativas falhas.
- **Bloqueio**: O IP ou usuário é bloqueado por **1 hora** após atingir o limite.
- **Reset**: O contador é zerado após um login bem-sucedido.

### 📜 Política de Segurança de Conteúdo (CSP)
Implementamos cabeçalhos **CSP** para mitigar ataques de **XSS** (Cross-Site Scripting) e injeção de dados.
- Bloqueio de scripts de fontes desconhecidas.
- Restrição de estilos e fontes apenas a domínios confiáveis (Google Fonts).
- Compatibilidade total com o workflow de desenvolvimento **Vite/React**.

### 🚥 Limitação de Taxa (API Throttling)
Para evitar abusos e ataques de negação de serviço (DoS) na API:
- **Anônimos**: Limite de 100 requisições/dia.
- **Usuários Autenticados**: Limite de 1000 requisições/dia.

---

## 2. Segurança de Dados

### 🔑 Gestão de Senhas
- **ZXCVBN**: Utilizamos o algoritmo de estimativa de força de senha do Dropbox. Senhas fracas ou baseadas em padrões comuns são rejeitadas.
- **Hashing**: Senhas são armazenadas utilizando o algoritmo **PBKDF2** com SHA256 (padrão Django).

### 🔐 Comunicação (Produção)
Em ambiente de produção (`DEBUG=False`), as seguintes proteções são obrigatórias:
- **HSTS**: HTTP Strict Transport Security ativado por 1 ano.
- **SSL Redirect**: Redirecionamento automático de HTTP para HTTPS.
- **Secure Cookies**: Cookies de Sessão e CSRF marcados como `Secure` e `HttpOnly`.

---

## 3. Auditoria e CI/CD

O pipeline de Integração Contínua executa ferramentas de segurança em cada commit:
- **Bandit**: Varredura de vulnerabilidades no código Python.
- **Pip-audit**: Verificação de vulnerabilidades conhecidas em bibliotecas de terceiros.
- **Check --deploy**: Verificação de flags de segurança críticas do Django.

---

## 4. Reportando Vulnerabilidades

Se você encontrar uma falha de segurança, por favor, **não abra uma Issue pública**. Envie um e-mail para a equipe de segurança (contato@sige.edu.br) para que possamos aplicar o patch de forma privada.

*Última atualização: Abril de 2026*

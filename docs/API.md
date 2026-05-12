# 📚 API REST — Guia de Uso e Swagger

> **Atualizado:** Maio de 2026 | **Especificação:** OpenAPI 3.0 (drf-spectacular)

---

## 📌 Acesso à Documentação

| Interface | URL | Descrição |
|---|---|---|
| **Landing Page (TI)** | `/ti/api-docs/` | Visão geral e guia de uso |
| **Swagger UI** | `/api/schema/swagger-ui/` | Interface interativa para testes |
| **ReDoc** | `/api/schema/redoc/` | Documentação focada em leitura |
| **Schema YAML** | `/api/schema/` | Download da especificação bruta |

---

## 🔐 Autenticação (JWT)

A API utiliza **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt`.

### 1. Obtendo o Token
```http
POST /api/token/
Content-Type: application/json

{
  "username": "sua_matricula",
  "password": "sua_senha"
}
```

**Resposta:**
```json
{
  "access": "eyJhbGciOiJIUzI1...",
  "refresh": "eyJhbGciOiJIUzI1..."
}
```

### 2. Usando nas Requisições
```http
GET /api/v1/academico/turmas/
Authorization: Bearer eyJhbGciOiJIUzI1...
```

### 3. Renovando o Token (Antes de Expirar)
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1..."
}
```

---

## 🗂️ Estrutura dos Endpoints

| Módulo | Prefixo |
|---|---|
| Usuários / Perfis | `/api/v1/usuarios/` |
| Acadêmico | `/api/v1/academico/` |
| Financeiro | `/api/v1/financeiro/` |
| Saúde | `/api/v1/saude/` |
| Segurança (TI) | `/api/v1/seguranca/` |

---

## 🧪 Usando o Swagger UI para Testes

1. Acesse `/api/schema/swagger-ui/`.
2. Clique em **"Authorize"** (ícone de cadeado no topo).
3. Digite `Bearer <seu_access_token>` e confirme.
4. Localize o endpoint desejado e clique em **"Try it out"**.
5. Preencha os parâmetros e clique em **"Execute"**.

---

## 📡 Padrão de Respostas HTTP

| Código | Significado |
|---|---|
| `200 OK` | Requisição bem-sucedida |
| `201 Created` | Recurso criado com sucesso |
| `400 Bad Request` | Dados de entrada inválidos |
| `401 Unauthorized` | Token ausente ou inválido |
| `403 Forbidden` | Sem permissão para esta ação |
| `404 Not Found` | Recurso não encontrado |
| `500 Server Error` | Erro interno inesperado |

---

> [!TIP]
> Em desenvolvimento (`DEBUG=True`), o Swagger UI é acessível sem autenticação especial. Em produção, apenas membros autenticados com permissão de TI ou Staff podem acessar o schema.

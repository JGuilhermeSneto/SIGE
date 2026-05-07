# 📋 Plano de Mudança: Login de Aluno → Matrícula Real

## 1️⃣ Visão Geral
- **Objetivo**: Substituir o campo de login do aluno (email) por sua **matrícula** (código interno único) em todo o ecossistema SIGE.
- **Benefícios**:
    - Integração direta com dispositivos IoT (RFID, ESP32) que leem a matrícula.
    - Simplificação da autenticação no aplicativo móvel (login por número curto e fixo).
    - Redução de ambiguidades de email (endereços múltiplos, domínios diferentes).
- **Escopo**: Backend Django, bancos de dados, API REST, módulos IoT, app mobile (React Native) e documentação.

---

## 2️⃣ Impacto nas Camadas
| Camada | Impacto | Comentário |
|---|---|---|
| **Modelo `Aluno`** | Campo `email` → `matricula` (char, unique). | Manter `email` opcional para comunicação, mas não como credencial. |
| **Auth Backend** | Custom `UsernameModelBackend` usando `matricula` como `USERNAME_FIELD`. |
| **Formulários** | Atualizar `LoginForm`, `RegistroForm` para validar matrícula. |
| **Serializers / API** | Alterar `AlunoSerializer` e endpoints de login (`/api/v1/auth/`). |
| **IoT** | Dispositivo enviará `matricula` ao tópico MQTT (`sige/iot/login`). |
| **Mobile** | Tela de login passa a aceitar “Matrícula”. Ajuste de validação no cliente. |
| **Migração DB** | Script de migração para criar coluna `matricula`, popular com valores existentes. |
| **Testes** | Atualizar/Adicionar testes de auth, API, IoT, mobile. |
| **Documentação** | Atualizar READMEs, Swagger, diagramas. |

---

## 3️⃣ Passos de Implementação (Semana 2 de Maio)

### 3.1 Padrão de Matrícula: **YYYYTTTUUUU**
- `YYYY` = ano corrente (ex.: 2026)
- `TTT` = ID da turma, preenchido com zeros à esquerda (3 dígitos)
- `UUUU` = ID do usuário/aluno, preenchido com zeros à esquerda (4 dígitos)

### 3.2 Backend Django
1. **Alterar modelo** `apps/usuarios/models/aluno.py`:
   ```python
   class Aluno(AbstractUser):
       matricula = models.CharField(max_length=12, unique=True)
       USERNAME_FIELD = "matricula"
       REQUIRED_FIELDS = []
   ```
2. **Criar migration**: `python manage.py makemigrations usuarios && python manage.py migrate`
3. **Populate `matricula`**:
   - Script `scripts/populate_matricula.py`:
   ```python
   from datetime import datetime
   def gerar_matricula(aluno):
       ano = datetime.now().year
       turma_id = f"{aluno.turma.id:03d}" if hasattr(aluno, "turma") else "000"
       user_id = f"{aluno.id:04d}"
       return f"{ano}{turma_id}{user_id}"
   ```
4. **Custom Auth Backend**: Configurar para buscar por `matricula` no `settings.py`.

### 3.3 API & IoT
- [ ] Endpoint de login receber `matricula` e `senha`.
- [ ] MQTT Topic: `sige/iot/login/{matricula}`.

### 3.4 Mobile (React Native)
- [ ] Atualizar `LoginScreen.js` para campo "Matrícula".

---
*Este plano detalha a transição crítica de identidade do sistema.*

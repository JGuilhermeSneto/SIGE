# 🧪 Testes Automatizados — SIGE

> **Atualizado:** Maio de 2026 | **Status:** 45/45 testes passando ✅ | **Cobertura:** ~55%

---

## 🏃 1. Executando os Testes

### Rodar todos os testes
```bash
pytest
```

### Com relatório de cobertura
```bash
pytest --cov=apps --cov-report=html
```
O relatório HTML será gerado em `htmlcov/index.html`.

### Rodar um módulo específico
```bash
pytest apps/academico/
pytest apps/financeiro/tests/
```

---

## 📊 2. Cobertura Atual por Módulo

| Módulo | Cobertura | Meta | Prioridade |
|---|---|---|---|
| `apps.usuarios` | ~70% | 80% | 🟠 Alta |
| `apps.academico` | ~65% | 80% | 🟠 Alta |
| `apps.financeiro` | ~50% | 75% | 🟡 Média |
| `apps.seguranca` | ~60% | 80% | 🟠 Alta |
| `apps.saude` | ~25% | 60% | 🔴 Crítica |
| `apps.dashboards` | ~28% | 60% | 🔴 Crítica |
| **TOTAL GLOBAL** | **~55%** | **75%** | — |

---

## 🛠️ 3. Configuração

O Pytest é configurado via `pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_test.py
```

O arquivo `conftest.py` na raiz define fixtures globais (usuários de teste, cliente autenticado, etc.).

---

## 🎯 4. Próximos Alvos de Cobertura

Os arquivos com 0% de cobertura são os de maior impacto para a próxima sprint:
- `apps/financeiro/services/financeiro_service.py`
- `apps/usuarios/services/perfil_service.py`
- `apps/saude/views.py`
- `apps/dashboards/views.py`

---

## ✅ 5. Tipos de Testes

| Tipo | Framework | Descrição |
|---|---|---|
| **Unitários** | Pytest + Mock | Testam funções e services isolados |
| **Integração** | Pytest + Django TestClient | Testam views e fluxos de URL |
| **Segurança** | Bandit (CI) | Varredura estática de vulnerabilidades |
| **E2E** | Planejado (Playwright) | Fluxos completos de matrícula e notas |

> [!NOTE]
> A meta de 75% de cobertura global está prevista para Q2/2026. Foque nos módulos de `services/` e `views.py` para máximo impacto por linha escrita.

# 📊 Guia de Monitoramento e Observabilidade — SIGE

O SIGE utiliza uma arquitetura de monitoramento em multicamadas (Multi-Layer Observability) para garantir a estabilidade do sistema, a performance de rede e a conformidade com a **LGPD**.

---

## 1. Observabilidade Industrial (Grafana + Prometheus) 🚀
Esta é a nossa "Torre de Controle" para métricas de infraestrutura em tempo real.

- **Prometheus**: Coleta métricas do Django (tempo de resposta, status 200/404/500, uso de CPU).
- **Grafana**: Painel visual para análise de dados técnicos.
- **Acesso**: [http://localhost:3000](http://localhost:3000) (admin/admin).
- **Métricas Chave**:
    - `django_http_requests_total_by_view`: Quais páginas são as mais acessadas.
    - `django_db_query_duration_seconds`: Tempo médio de resposta do banco de dados.
    - `process_resident_memory_bytes`: Uso de memória do servidor.

---

## 2. Monitoramento de Erros (Sentry) 👁️
O **Sentry** captura exceções de código e falhas de performance antes que o usuário as perceba.

- **O que é monitorado**:
    - Erros 500 (Internal Server Errors).
    - Consultas SQL N+1 e Transações lentas.
- **Integração**: Configurado em `config/settings.py` via `SENTRY_DSN`.

---

## 3. Mensageria e Filas (RabbitMQ Management) 🐇
O monitoramento das tarefas em segundo plano (Celery) é feito via RabbitMQ.

- **Painel de Gestão**: [http://localhost:15672](http://localhost:15672) (guest/guest).
- **Uso**: Verificar se tarefas de geração de PDF ou envio de e-mails estão acumuladas ou falhando.

---

## 4. Auditoria LGPD (Acessos Sensíveis) 🛡️
Middleware que registra acessos a dados sensíveis (Saúde, Financeiro, Documentos).

- **Tabela**: `comum.AuditLog`.
- **Campos**: Usuário, IP, Caminho acessado e Timestamp.
- **Finalidade**: Conformidade legal e trilha de segurança.

---

## 5. Trilha Histórica (Simple History) 📜
Para tabelas críticas (Alunos, Faturas, Patrimônio).
- Permite ver o histórico de alterações ("Quem mudou o quê e quando") diretamente no Django Admin através do botão **"Histórico"**.

---

## 6. Segurança Anti-Brute Force (Django Axes) 🔒
Monitora e bloqueia tentativas de login suspeitas.
- **Comandos Úteis**:
    ```bash
    python manage.py axes_list_attempts  # Lista IPs suspeitos
    python manage.py axes_reset          # Limpa bloqueios
    ```

---

## 7. Dashboard de Inteligência Acadêmica (BI) 🧠
Focado no gestor escolar para tomada de decisão baseada em dados.
- **Evasão Preditiva**: Modelos de risco em tempo real.
- **KPIs de Saúde**: Distribuição sanguínea e alertas de alergia.
- **Performance**: Médias globais por turma.

---

> **Regra de Ouro**: "Observabilidade não é opcional." — Toda nova funcionalidade deve estar mapeada no Grafana ou no Sentry.

*Última atualização: 27 de Abril de 2026 — Padrão Jarvis de Observabilidade Industrial.*

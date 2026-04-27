# 🏗️ Guia de Infraestrutura SIGE (RabbitMQ + Monitoramento)

Este documento descreve como operar a nova infraestrutura do SIGE utilizando Docker, Celery e o stack de monitoramento.

## 🚀 Como Iniciar

Certifique-se de ter o **Docker** e o **Docker Compose** instalados.

1.  **Construir e Subir os Containers:**
    ```bash
    docker-compose up --build
    ```

2.  **Verificar se tudo está rodando:**
    *   **Django App**: [http://localhost:8000](http://localhost:8000)
    *   **RabbitMQ Dashboard**: [http://localhost:15672](http://localhost:15672) (guest/guest)
    *   **Prometheus**: [http://localhost:9090](http://localhost:9090)
    *   **Grafana**: [http://localhost:3000](http://localhost:3000) (admin/admin)

---

## 🐇 RabbitMQ & Celery

O RabbitMQ agora gerencia as tarefas assíncronas do sistema (como geração de PDFs pesados e envios de e-mail).

*   **Broker**: `amqp://guest:guest@rabbitmq:5672//`
*   **Worker**: O serviço `worker` no docker-compose já inicia automaticamente o consumo das filas.
*   **Monitoramento de Filas**: Acesse a aba "Queues" no painel do RabbitMQ para ver as mensagens sendo processadas.

---

## 📊 Monitoramento (Grafana + Prometheus)

Para visualizar as métricas do Django no Grafana, siga estes passos na primeira vez:

1.  **Adicionar Data Source no Grafana**:
    *   Vá em **Connections > Data Sources**.
    *   Clique em **Add data source** e escolha **Prometheus**.
    *   No campo URL, digite: `http://prometheus:9090`.
    *   Clique em **Save & Test**.

2.  **Importar Dashboard do Django**:
    *   Vá em **Dashboards > New > Import**.
    *   Use o ID `9528` (Dashboard padrão para Django-Prometheus).
    *   Selecione o Data Source do Prometheus que você criou.

### Métricas Disponíveis:
*   `django_http_requests_total_by_view_transport_method_total`: Total de acessos por página.
*   `django_db_query_duration_seconds_bucket`: Tempo de resposta do banco de dados.
*   `process_cpu_seconds_total`: Uso de CPU do servidor Django.

---

## 🛠️ Comandos Úteis

*   **Reiniciar apenas o Worker**: `docker-compose restart worker`
*   **Ver logs em tempo real**: `docker-compose logs -f`
*   **Limpar volumes do banco**: `docker-compose down -v` (Cuidado: apaga os dados!)

---

**Nota**: Em ambiente de desenvolvimento local (fora do Docker), o sistema ainda tentará buscar o RabbitMQ no `localhost:5672`. Se não tiver o RabbitMQ instalado localmente, utilize o Docker Compose.

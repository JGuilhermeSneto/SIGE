# 🧠 Hub de Inteligência & Relatórios (Dashboards)

Este aplicativo é o motor analítico central do SIGE. Ele unifica o **BI Acadêmico** e a **Central de Relatórios** em uma interface única de alto nível para gestores.

## 🚀 Funcionalidades Chave

- **Visão Analítica (BI)**: Gráficos dinâmicos de Evasão Preditiva, Status de Matrícula e Performance por Turma.
- **Central de Relatórios**: Emissão rápida de documentos oficiais (Histórico Escolar, Boletins) e exportações massivas em CSV.
- **Inteligência de Saúde**: Monitoramento de indicadores de inclusão (PCD) e alertas médicos em tempo real.
- **Exportação Master**: Geração de dossiês gerenciais em PDF com QR Code de autenticidade.

## 🏗️ Arquitetura Técnica

- **Lógica de Leitura (Selectors)**: Centralizada em `selectors.py` para garantir que o dashboard carregue em milissegundos, independente do tamanho da base.
- **Motor de PDF**: Utiliza `utils/pdf_engine.py` (ReportLab) para geração de documentos industriais.
- **Frontend**: Dashboards baseados em **Chart.js** com suporte a temas e glassmorphism.

## 🔗 Integrações
- **Monitoramento**: Exporta métricas de performance para o Prometheus.
- **Processamento**: Utiliza RabbitMQ/Celery para exportações de longa duração.

> Atualizado em 2026-04-27 — Unificação do Hub de Inteligência concluída.

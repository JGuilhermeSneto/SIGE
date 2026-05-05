# ⚙️ Núcleo de Configuração & Orquestração

O diretório `config/` é o sistema nervoso central do SIGE, onde a orquestração de serviços, segurança de alto nível e integração de middleware são definidas.

## 🏗️ Gestão de Ambiente (Twelve-Factor App)
- **Settings Dinâmico**: Utiliza `python-decouple` para separar código de configuração.
- **Produção (Render + Aiven)**: Configurações otimizadas para MySQL (Aiven) e Cache Redis com WhiteNoise para estáticos.
- **Observabilidade**: Integração nativa com **Sentry** e **Prometheus** injetada via Middleware.

## 🛡️ Pilares de Segurança
- **CORS & CSP**: Políticas restritas de segurança de conteúdo para mitigar ataques XSS.
- **JWT & Auth**: Configuração industrial de SimpleJWT com blacklist de tokens.
- **Axes & Locks**: Proteção contra força bruta configurada em nível de kernel Django.

## 🚀 Orquestração de Tarefas
- **Celery**: Configurações de Broker (RabbitMQ) e Result Backend centralizadas para processamento assíncrono em larga escala.

> Atualizado em Maio de 2026 — Orquestração de Produção (Render) consolidada.


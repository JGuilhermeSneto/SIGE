# 📢 Módulo de Comunicação & Mural Institucional

O app `apps.comunicacao` centraliza o fluxo de informações da escola, garantindo que avisos, comunicados e eventos cheguem ao público correto de forma instantânea.

## 📐 Estrutura de Dados (Models)
- `Comunicado`: O núcleo da mensagem. Suporta formatação rica e anexos.
- `PublicoAlvo`: Segmentação dinâmica (Alunos, Professores, Gestores, Responsáveis ou Turmas específicas).
- `CanalComunicacao`: Definição de onde a mensagem aparece (Mural, E-mail ou Notificações Push).

## 🚀 Engenharia e UI/UX
- **Segmentação Inteligente**: A lógica de visibilidade garante que um comunicado para o "3º Ano A" seja visível apenas para os envolvidos, otimizando o ruído de informação.
- **Mural "Premium"**: Interface inspirada em feeds modernos, com cards glassmorphism e suporte a imagens de destaque.
- **Processamento Assíncrono**: O envio de comunicados em massa via e-mail é delegado ao **Celery/RabbitMQ**, mantendo a interface rápida.

## 🔗 Integração Acadêmica
- Conexão direta com o `apps.academico` para extração de listas de turmas e perfis de usuários em tempo real.

> Atualizado em Maio de 2026 — Mural Premium e Segmentação por Turma consolidados.


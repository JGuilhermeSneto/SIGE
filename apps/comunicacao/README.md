# 💬 App: Comunicação (v1.0)

Módulo de mensagens internas e notificações do SIGE.

![Testes](https://img.shields.io/badge/Testes-Parcial-orange?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~50%25-orange?style=flat-square)

## Responsabilidades
- Mensagens internas entre usuários do sistema
- Comunicados institucionais (gestores → toda escola)
- Notificações automáticas por eventos (notas, chamadas, atividades)
- Histórico de conversas e leitura de mensagens

## Modelos Principais
- `Mensagem`, `Conversa`, `Comunicado`

## Permissões
- **Gestor**: envio de comunicados para toda a escola
- **Professor**: mensagens para alunos e responsáveis da turma
- **Aluno/Responsável**: mensagens individuais

## ⚠️ Status QA (v8.0 Apex)
A suíte de testes de comunicação está em estabilização parcial. Uma das views apresenta falhas de permissão que estão na fila de correção.

| Área | Status |
|---|:---:|
| Listagem de mensagens | ✅ Estável |
| Envio de mensagens | ⚠️ Em correção |

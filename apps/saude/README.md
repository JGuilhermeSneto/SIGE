# 🏥 App: Saúde (v1.2)

Módulo de saúde escolar e gestão médica do SIGE.

![Testes](https://img.shields.io/badge/Testes-Parcial-orange?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~50%25-orange?style=flat-square)

## Responsabilidades
- Ficha médica de alunos (tipagem sanguínea, alergias, plano de saúde)
- Gestão e aprovação de atestados médicos
- Alertas de saúde e notificações para gestores
- Histórico de ocorrências de saúde

## Modelos Principais
- `FichaMedica`, `Atestado`, `OcorrenciaSaude`

## Permissões
- **Gestor/Enfermagem**: visão e gestão completa
- **Aluno**: envio de atestados e visualização da própria ficha
- **Responsável**: acesso à ficha do dependente

## ⚠️ Status QA (v8.0 Apex)
A suíte de testes do módulo de saúde está em estabilização parcial. Falhas identificadas em views de envio de atestado e visualização de ficha médica por aluno — na fila de correção para próxima iteração.

| Área | Status |
|---|:---:|
| Ficha médica (model) | ✅ Estável |
| Visualização gestor | ⚠️ Em correção |
| Envio de atestado | ⚠️ Em correção |
| Listagem atestados | ⚠️ Em correção |

# 💰 App: Financeiro (v1.4)

Módulo de gestão financeira escolar do SIGE.

![Testes](https://img.shields.io/badge/Testes-Parcial-orange?style=flat-square&logo=pytest)
![Cobertura](https://img.shields.io/badge/Cobertura-~55%25-orange?style=flat-square)

## Responsabilidades
- Controle de mensalidades, faturas e inadimplência
- BI financeiro com indicadores de receita e projeções
- Integração com gateway de pagamentos
- Relatórios de fluxo de caixa e auditoria financeira

## Modelos Principais
- `Fatura`, `Pagamento`, `Contrato`, `PlanoFinanceiro`

## Permissões
- **Gestor/Financeiro**: acesso total ao módulo
- **Responsável**: visualização das próprias faturas

## ⚠️ Status QA (v8.0 Apex)
A suíte de testes do módulo financeiro está em estabilização parcial. Algumas views de listagem de faturas e painel financeiro apresentam falhas de fixture/CPF que estão na fila de correção para a próxima iteração.

| Área | Status |
|---|:---:|
| Seletores financeiros | ✅ Estável |
| Segurança financeira | ✅ Estável |
| Views de painel | ⚠️ Em correção |
| Views de faturas | ⚠️ Em correção |

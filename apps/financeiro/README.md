# 💰 App: Financeiro

Módulo de gestão financeira da instituição — mensalidades, faturas e pagamentos.

## Responsabilidades
- Geração de faturas mensais por aluno
- Controle de pagamentos e inadimplência
- Relatórios financeiros para gestão
- Integração futura com Gateway de Pagamento (Asaas/Efí)

## Modelos Principais
- `Fatura`, `Pagamento`
- `PlanoFinanceiro`, `DescontoFinanceiro`

## Permissões
- **Responsável**: visualiza faturas e comprovantes do dependente.
- **Gestor**: cria, edita e baixa faturas; acessa relatórios globais.

## Roadmap
- [ ] Integração com Pix (Asaas/Efí)
- [ ] Webhook para baixa automática de faturas
- [ ] Geração de NF-e de serviços

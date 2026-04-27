# 💰 Módulo Financeiro & BI Contábil

O Módulo Financeiro do SIGE é o motor de **Business Intelligence** que acompanha a saúde contábil da instituição. Ele cruza faturas, folha de pagamento e despesas de infraestrutura.

## 📐 Estrutura de Dados (Models)

- `Lancamento`: O **Livro Diário**. Centraliza todas as entradas e saídas.
- `Fatura`: Contas a receber (Mensalidades). Status: `PENDENTE`, `PAGO`, `ATRASADO`.
- `FolhaPagamento`: Gestão mensal de salários de Professores e Gestores.
- `CentroCusto` & `CategoriaFinanceira`: Classificação contábil para DRE.

## 🚀 Engenharia Financeira

- **FinanceiroService**: Orquestra operações críticas (Baixa de faturas, geração de folha) sob transações atômicas.
- **FinanceiroSelector**: Camada de leitura otimizada para geração de DRE e Fluxo de Caixa.
- **Segurança**: Valores sensíveis são protegidos por criptografia **AES/Fernet** no nível do banco de dados.

## 📊 Inteligência de Negócio
- **Dashboard Gerencial**: Integrado ao Hub de Inteligência, fornecendo KPIs de:
    - Inadimplência Real vs. Esperada.
    - DRE Dinâmico (Receitas × Despesas).
    - Projeção de Fluxo de Caixa.

## 🛣️ Próximos Passos
- **Gateway Asaas/Efí**: Integração via Webhooks para baixa automática de Pix e Boletos.
- **Régua de Cobrança**: Notificações automáticas via Celery/RabbitMQ para faturas vencidas.

# 💰 Módulo Financeiro & Inteligência de Negócios (BI)

O Módulo Financeiro do SIGE não é apenas um emissor de boletos, mas um motor de **Business Intelligence (BI)** completo que acompanha a saúde contábil da instituição de ensino. Ele cruza faturas pagas e pendentes com a folha de pagamento de servidores e as despesas de infraestrutura.

## 📐 Arquitetura de Dados (Models)

- `CategoriaFinanceira`: Tabela central de classificação contábil (Ex: *Receita - Mensalidades*, *Despesa - Energia Elétrica*).
- `CentroCusto`: Agrupador de despesas (Ex: *Pedagógico*, *Administrativo*, *TI*).
- `Fatura`: As "Contas a Receber" emitidas contra os alunos. Podem estar nos status `PENDENTE`, `PAGO` ou `ATRASADO`.
- `Pagamento`: A liquidação física de uma Fatura (via PIX, Boleto ou Cartão). 
- `Lancamento`: O **Livro Diário**. Toda entrada ou saída de caixa (inclusive a folha de pagamento ou pagamento de faturas) gera um lançamento no caixa geral, associado a uma `CategoriaFinanceira` e um `CentroCusto`.
- `FolhaPagamento`: Registro mensal consolidado do RH (salário base, descontos, bônus) para professores e gestores.

## 🚀 Integração com o Ecossistema

1. **Gateways de Pagamento (Futuro)**: O model `Fatura` possui campo criptografado `link_pagamento` preparado para receber links gerados pelas APIs do Asaas/Efí.
2. **Dashboard Gerencial (Gestor)**: A view agrega dados do Livro Diário (`Lancamento`) para montar gráficos comparativos de DRE (Demonstrativo de Resultado do Exercício) e fluxo de caixa na tela inicial do Superusuário.
3. **Painel do Aluno em Tela Cheia**: Os alunos possuem atalhos dinâmicos (verde) injetados direto no topo do painel principal (sem menu lateral) para acessarem o carnê de mensalidades a qualquer momento.

## 🛠️ Trilha de Auditoria

Todas as tabelas de alta sensibilidade (como `Lancamento` e `Pagamento`) usam o `django-simple-history` para registrar quem alterou um valor, quando foi alterado e qual era a quantia original.

## 🧑‍💻 Para Desenvolvedores

Se você for testar gráficos e queries neste módulo, certifique-se de ter rodado o script principal de sementes:
```bash
python seed_db.py
```
Esse script gera um loop de 10 anos, produzindo faturas fictícias retroativas e gerando pagamentos com datas passadas para que os gráficos anuais de BI fiquem preenchidos com "dados orgânicos".

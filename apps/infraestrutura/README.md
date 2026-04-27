# 🏢 Módulo de Infraestrutura, Estoque e Patrimônio

Este módulo gerencia o patrimônio durável e os itens consumíveis (almoxarifado) da instituição. Recentemente refatorado para o padrão **Clean Architecture**, garantindo alta performance e integridade de dados.

## 📐 Arquitetura de Dados (Models)

- `UnidadeEscolar` & `Ambiente`: Representam a estrutura física da escola.
- `ItemPatrimonio`: Bens duráveis com controle de tombamento e criptografia de valor.
- `ManutencaoBem`: Registro de ordens de serviço e histórico de reparos.
- `ItemEstoque` & `SaldoEstoque`: Controle de saldos de itens consumíveis com gatilhos de reposição mínima.

## 🧠 Padrões de Projeto (Refatoração 2026)

O módulo segue agora a separação estrita de responsabilidades:

### 1. Camada de Leitura (Selectors) — `selectors.py`
Utiliza o **Selector Pattern** para centralizar consultas complexas e cálculos de BI:
- `InfraSelector.get_painel_metrics()`: Retorna KPIs de patrimônio e estoque.
- `InfraSelector.get_estoque_critico()`: Filtra itens abaixo do saldo mínimo com `O(1)`.

### 2. Camada de Escrita (Services) — `services/`
Centraliza a lógica de negócio e garante transações atômicas:
- `EstoqueService.registrar_movimentacao()`: Atualiza o saldo físico e cria o log de movimentação em uma única transação segura.

## 💡 Integrações Internas
- **Financeiro**: Gastos com manutenção geram lançamentos automáticos no Livro Diário.
- **Dashboards**: Dados de infraestrutura são consumidos pelo Hub de Inteligência via Selectors.

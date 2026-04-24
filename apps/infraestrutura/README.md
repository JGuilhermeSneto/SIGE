# 🏢 Módulo de Infraestrutura, Estoque e Patrimônio

Um braço do SIGE focado na operação material da instituição. Ele previne que a escola fique sem folhas de ofício no almoxarifado ou perca o controle do tombamento de seus laboratórios de TI.

## 📐 Arquitetura de Dados (Models)

- `UnidadeEscolar` & `Ambiente`: O campus principal e a divisão das salas e setores.
- `ItemPatrimonio` (O Inventário Durável): Trata das cadeiras, microscópios e datashows. Eles possuem um número de tombamento protegido. A lógica de Banco de Dados criptografa via `AES` o campo de `valor_aquisicao` em banco para evitar vazamentos contábeis a quem possua acessos diretos SQL.
- `ManutencaoBem`: Um livro de manutenções indicando as requisições de conserto e troca de itens estragados do patrimônio.
- `ItemEstoque` & `SaldoEstoque`: Os consumíveis da escola (sabonete, café, papel) configurados com gatilhos de `estoque_minimo`.
- `MovimentacaoEstoque`: A rastreabilidade contínua (Entradas e Saídas) consumidas pelos setores.

## 💡 Integração 

- Os gastos gerados em `ManutencaoBem` e em compras de novos móveis são projetados para interagir diretamente com o **Módulo Financeiro**, registrando as quantias no `Lancamento` do Livro Diário com seus respectivos Centro de Custos.

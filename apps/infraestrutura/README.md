# 🏭 App: Infraestrutura

Módulo de gestão de patrimônio, almoxarifado e recursos físicos da instituição.

## Responsabilidades
- Cadastro e controle de patrimônio (equipamentos, móveis)
- Gestão de estoque do almoxarifado
- Solicitações de recursos e materiais
- Relatórios de inventário

## Modelos Principais
- `ItemPatrimonio`, `CategoriaPatrimonio`
- `ItemEstoque`, `MovimentacaoEstoque`
- `SolicitacaoRecurso`

## Arquitetura
Utiliza **Clean Architecture** com camada de Service e Selectors separados das Views.

## Permissões
- **Gestor de Infraestrutura**: controle total de patrimônio e almoxarifado.
- **Outros perfis**: podem fazer solicitações de recursos.

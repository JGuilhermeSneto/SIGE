# SIGE · Forms

Definição de formulários Django para entrada e validação de dados, organizados por domínio funcional.

## Arquivos e Responsabilidades

- **`base.py`**: ModelForms básicos e mixins de validação comum.
- **`perfis.py`**: Formulários complexos para Cadastro de Professores, Alunos e Gestores, lidando com o salvamento simultâneo do `User` e do modelo de perfil.
- **`academico.py`**: Formulários para criação de Disciplinas e Turmas.
- **`autenticacao.py`**: Customizações de formulários de login ou recuperação de senha, se necessário.

## Observações para Manutenção

- Ao criar novos formulários, siga o padrão de estilização de widgets para garantir que os campos herdem as classes de design premium (ex: `form-control`).
- Implemente validações customizadas no método `clean()` para garantir integridade dos dados antes de salvar no banco.

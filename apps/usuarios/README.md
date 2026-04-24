# 👤 Módulo de Autenticação e Perfis (Usuarios)

O componente base do sistema de controle de acesso (RBAC - Role Based Access Control) do SIGE.

## 📐 Perfis Polimórficos

Para garantir que o Django gerencie senhas nativamente, enquanto as informações extras sejam independentes, utilizamos o conceito de OneToOne com a base abstrata `PessoaBase`:
- **`Gestor`**: Acesso completo e aprovações sensíveis (ex: Atestados e Faturas).
- **`Professor`**: Gerenciamento de seu diário e turma, mas sem acesso à matriz financeira do aluno ou às abas do diretor.
- **`Aluno`**: Entidade consumidora final. Restrita a visualização de notas e faturas.

## 🔒 Segurança

Todo o acesso ao sistema trafega pelo controle de sessões e cookies seguros definidos no `settings.py` (ou em tokens JWT se utilizando a API exposta em `apps/api/`). O painel universal renderiza conteúdos baseados no grupo / propriedade da classe atual via `if has_attr`.

## 🧑‍💻 Automação de Histórico
Os `Alunos` carregam o campo de `status_matricula` (`ATIVO`, `INATIVO`, `FORMADO`, `EVADIDO`, `TRANSFERIDO`). Se você criar dados usando o script `seed_db.py`, ele irá gerar perfis com esses status que interagem diretamente com o fechamento do histórico escolar no app Acadêmico.

# 📚 Módulo de Biblioteca (SIGE)

Bem-vindo ao módulo de **Biblioteca Escolar** do Sistema Integrado de Gestão Escolar (SIGE). Este módulo funciona como a central de acervo literário e de pesquisa dos alunos e professores, modernizando o fluxo de leitura e empréstimos de obras na instituição de ensino.

## 🌟 Funcionalidades e Regras de Negócio

1. **Gestão de Acervo Literário**
   - Controle total do catálogo de livros por autor, categoria/diretriz e disponibilidade física (quantidade em estoque).
   - Suporte a ISBN e catalogação sistemática.

2. **Fluxo de Reservas (Painel do Aluno)**
   - O aluno pode consultar o catálogo da biblioteca online diretamente no seu painel pelo botão `Biblioteca`.
   - Limite parametrizado de no máximo **2 (dois) livros simultâneos** por aluno em seu portal.
   - Qualquer tentativa de reserva além do limite ou no caso de indisponibilidade de estoque é bloqueada automaticamente pelo ORM do sistema, garantindo consistência no lado do *backend* e *frontend*.

3. **Confirmação e Devolução (Painel do Gestor)**
   - O bibliotecário ou o Gestor Escolar utiliza o painel interno para aprovar ou rejeitar uma reserva de interesse.
   - Todo fluxo de data de aprovação, expiração do período e momento de devolução é registrado com logs precisos no banco de dados.
   
## 💻 Integração com Django e Frontend

Este app segue a arquitetura **MTV** padrão do projeto SIGE. Além da interface integrada e renderizada via server-side com `apps/biblioteca/templates/`, as rotas internas expostas podem e devem ser mapeadas ao Frontend em React (PWA Vite).

### Rotas e Views Principais
- `/biblioteca/`: Catálogo geral e portal digital.
- `/biblioteca/meus-livros`: Controle de empréstimos sob posse do aluno.
- `/biblioteca/gestao/`: Painel de administração de acervo.

## 🚀 Próximos Passos (Roadmap de Evolução)
- Alertas dinâmicos via `NotificacaoAluno` (Módulo de Desempenho) sempre que a data de devolução do livro estiver próxima a expirar.
- Integração de ePubs ou acervo Open Source digital direto no módulo web.

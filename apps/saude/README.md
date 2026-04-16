# 🏥 Módulo de Saúde Escolar (SIGE)

Bem-vindo ao módulo de **Saúde do Aluno** dentro do Sistema Integrado de Gestão Escolar (SIGE). Este módulo foi desenhado para assegurar o amparo clínico, a segurança integrativa e o registro vacinal dos estudantes enquanto estes frequentam as imediações da escola.

## 🌟 Funcionalidades e Regras de Negócio

1. **Ficha Médica Base e Alertas**
   - Criação de ficha médica acoplada ao Perfil do Aluno (Relação `OneToOneField`).
   - Mapeamento detalhado do Tipo Sanguíneo e Contato Telefônico de Emergência.
   - **Campos Vitais de Risco**: Inserção de dados para Medicamentos de uso contínuo, Condições de PCD (Pessoas com Deficiência) e **Alergias severas**. Esses campos desencadeiam ícones de alerta visual no Painel do Professor ao lado do nome do estudante na listagem da pauta.

2. **Carteira de Vacinação**
   - Banco de registros integrados atrelados à ficha médica para monitoramento de vacinações essenciais e o envio de lotes sazonais.

3. **Arquitetura de Permissões**
   - O acesso a informações clínicas é tratado com extremo sigilo. A view `visualizar_saude_aluno` e o painel correspondente só serão abertos nas seguintes condições:
     - 🎓 **Para o Próprio Estudante**: O aluno tem o direito inalienável de ver seu próprio prontuário gerado pelo estado acadêmico (`eh_proprio_aluno`).
     - 👨‍🏫 **Professor Ativo na Turma**: O professor tem autorização de consulta clínica APENAS aos alunos que leciona disciplinas do seu grade curricular do ano letivo. O acesso a alunos de outras classes é criptograficamente evitado.
     - 👔 **Gestor Escolar**: Acesso administrativo Master-level podendo editar e preencher as tabelas no painel `editar_ficha_medica`.

## 💻 Integração e Design System
O front-end utiliza o esquema dinâmico do `medical-card` e engrenagem isolada sem conflito temático, utilizando elementos do **Design System Premium** (Ícones Fa-solid com tons `Ruby` caso o aluno contenha alergias ou `Emerald/Cyan`).

## 🚀 Próximos Passos
- Refatoração dos alertas para inclusão em Módulos de Nutrição (Alimentação diferenciada em Refeitórios para alunos alérgicos/restrições).

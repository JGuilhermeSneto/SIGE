# Metodologia de Parametrização dos Dados com Base nos Microdados do INEP (Censo Escolar)

**Projeto:** ELISE — Módulo de Inteligência Artificial e Apoio à Decisão (DSS)  
**Documento Acadêmico:** Monografia de TCC (Seção 5.2 — Dados Utilizados e Preparação do Ambiente Experimental)  
**Fonte Primária de Referência:** Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).  
*Microdados da Educação Básica / Censo Escolar*. Disponível em: <https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados>.

---

## 1. Justificativa Metodológica e Ética (LGPD)

Conforme estabelecido no **Art. 20 da Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018)** e no projeto de pesquisa do TCC (Seção 3.2 e 5.1):
1. **Anonimização e Não Utilização de Dados Pessoais Sensíveis:** Para resguardar a privacidade de estudantes e servidores e cumprir os preceitos de privacidade por design (*Privacy by Design*), o protótipo não utiliza dados reais identificáveis de pessoas físicas (sem CPF, notas individuais discriminadas, prontuários de saúde ou registros de faltas nominais).
2. **Representatividade Estatística:** Em substituição a registros reais confidenciais, o protótipo utiliza um modelo de instituição escolar de ensino básico privada parametrizado diretamente nas médias e frequências observadas nos **Microdados do Censo da Educação Básica do INEP**.

---

## 2. Parâmetros Extraídos dos Microdados do Censo Escolar (INEP)

Os microdados do INEP trazem o perfil detalhado de estabelecimentos de ensino no Brasil (`microdados_ed_basica`). O recorte institucional adotado para a escola-piloto simulada no ELISE baseia-se em uma **escola privada de porte médio (código de dependência administrativa `TP_DEPENDENCIA = 4`)**, com as seguintes características:

| Variável INEP | Descrição no Censo Escolar | Valor Parametrizado no Protótipo ELISE | Tabela / Modelo Django SIGE |
| :--- | :--- | :--- | :--- |
| `QT_MAT_BAS` | Matrículas totais na educação básica | **245 alunos matriculados** | `core_aluno` |
| `QT_TUR_BAS` | Número total de turmas/turmas-ano | **33 turmas/anos ativos** | `core_turma` |
| `QT_DOC_BAS` | Número de docentes na educação básica | **15 professores especialistas** | `core_professor` |
| `IN_DISC_*` | Componentes curriculares obrigatórios (BNCC) | **12 disciplinas da BNCC por nível** (264 alocações disciplina-turma) | `core_disciplina` |
| `QT_SALAS_UTILIZADAS` | Salas de aula e ambientes pedagógicos | **7 ambientes principais** (salas regulares, laboratório, biblioteca, quadra) | `infra_ambiente` |
| `IN_BIBLIOTECA` | Presença de biblioteca escolar na entidade (`1 = Sim`) | **Ativo (`IN_BIBLIOTECA=1`)** | `biblioteca_livro` / `infraestrutura_unidadeescolar` |
| `QT_LIVROS_ACERVO` | Média de acervo para escolas privadas de porte médio | **200 títulos cadastrados / 796 exemplares físicos** | `biblioteca_livro` |
| `QT_EQUIP_*` | Equipamentos de informática, climatização e mobiliário | **250 itens patrimoniais catalogados** | `infra_patrimonio` |
| `TP_SITUACAO_PAG` | Indicadores de sustentabilidade e adimplência | **2.880 títulos/faturas financeiras** (histórico agregado) | `fin_fatura` |

---

## 3. Mapeamento de Entidades do Sistema e Rastreabilidade (Quadro 6 do TCC)

O Quadro 6 da monografia detalha as entidades acessadas pelo assistente de IA:

| Entidade | Total no Banco | Dados Acessados pelo Assistente | Dados Excluídos (LGPD / Sigilo) |
| :--- | :---: | :--- | :--- |
| **Turmas (`core_turma`)** | 33 | Nome, turno, ano letivo, total de alunos matriculados por turma | Nomes de alunos, situação socioeconômica |
| **Professores (`core_professor`)** | 15 | Formação acadêmica, especialização, área de atuação, contagem total | CPF, salário nominal, endereço, telefone |
| **Disciplinas (`core_disciplina`)** | 264 | Nome do componente curricular, carga, vínculo turma-professor | - |
| **Ambientes (`infra_ambiente`)** | 7 | Tipo (sala, laboratório, biblioteca), capacidade nominal, status | - |
| **Acervo / Livros (`biblioteca_livro`)** | 200 títulos (796 ex.) | Título, autor, editora, quantidade total, exemplares disponíveis | Histórico nominal de leitura de alunos |
| **Empréstimos (`biblioteca_emprestimo`)** | 132 | Status do empréstimo (ativo, atrasado, devolvido), datas de prazo | Identificação de qual aluno atrasou |
| **Patrimônio (`infra_patrimonio`)** | 250 | Quantidade total de bens, estado de conservação | - |
| **Financeiro (`fin_fatura`)** | 2.880 | Totais agregados (pagas, pendentes, atrasadas) | Dados bancários, nomes de responsáveis |

---

## 4. Garantia da Camada RAG Determinística

Nenhum cálculo estatístico ou agregação quantitativa é delegado ao modelo de linguagem (`llama3.1:8b`). O serviço `apps.ia.services.contexto.montar_contexto()` utiliza exclusivamente queries agregadas do Django ORM (`.count()`, `.aggregate(Sum(...))`, `.annotate(Count(...))`), assegurando que:
- O índice de alucinação numérica seja rigorosamente **0%**;
- Toda afirmação do assistente possa ser conferida diretamente via SQL / Django Admin;
- O tempo de recuperação dos dados institucionais ocorra em **menos de 50 milissegundos**, deixando o tempo de resposta prioritariamente para a geração da síntese em linguagem natural.

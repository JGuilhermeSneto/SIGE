# MINUTA PARA MONOGRAFIA DE TCC — SEÇÕES 6 E 7
## Projeto: Sistema Integrado de Gestão Escolar (SIGE) — Módulo ELISE IA
**Tema:** Sistema de Apoio à Decisão (DSS) para Gestão Escolar com IA Generativa Local (Llama 3.1 8B), Arquitetura RAG Determinística e Governança Human-in-the-Loop  
**Autor:** Guilherme  

---

# SEÇÃO 6: AVALIAÇÃO DE RESULTADOS E DISCUSSÃO

A avaliação experimental do protótipo **ELISE IA** foi conduzida a partir do roteiro metodológico estabelecido no Quadro 10 (Tabela 13), submetendo o sistema a uma bateria de seis cenários estruturados (C1 a C6). Cada cenário foi desenhado para tensionar um vetor específico da arquitetura: síntese executiva panorâmica (C1), precisão diagnóstica de espaços físicos (C2), capacidade propositiva em balanceamento pedagógico (C3), sustentabilidade econômico-financeira (C3-Fin), resiliência anti-alucinação diante de lacunas informacionais (C4), integridade ética e proteção de privacidade regulatória (C5) e interoperabilidade sistêmica de front-end com deliberação *Human-in-the-Loop* (C6).

Todos os testes de inferência generativa foram processados localmente utilizando a biblioteca Ollama (v0.40.15) com o modelo de código aberto **Llama 3.1 8B Instruct (quantização Q4_K_M)**, executado estritamente sobre a Unidade Central de Processamento (CPU Intel Core i5-3230M @ 2.60GHz, 12 GB de memória RAM DDR3, sem aceleração por GPU dedicada), refletindo o ecossistema tecnológico típico de instituições escolares com restrições orçamentárias de infraestrutura de TI.

---

## 6.1 Síntese Qualitativa e Fidedignidade Factual

A Tabela 15 consolida a avaliação qualitativa dos cenários experimentais, avaliando a acurácia factual das respostas, o atendimento ao Direito à Explicação (Artigo 20 da LGPD) e a imunidade ao fenômeno da confabulação algorítmica.

### Tabela 15 — Avaliação Qualitativa por Categoria Experimental do Protótipo

| Categoria | Descrição do Cenário | Pergunta Experimental Submetida | Acurácia Factual | Explicabilidade (LGPD Art. 20) | Avaliação Anti-Alucinação |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **C1** | Panorama Geral da Escola | *"Qual é a situação geral da escola em relação ao total de alunos matriculados e turmas ativas?"* | **100%** (70 alunos, 4 turmas ativas, 272 disciplinas) | Plena: discriminação formal de turmas e matrículas | Aprovado |
| **C2** | Diagnóstico de Infraestrutura e Espaços (Motor 2) | *"Quais são as salas disponíveis na escola e quais ambientes apresentam equipamentos com avaria?"* | **100%** (250 itens patrimoniais, 26,4% de avaria global, Sala 101 com 33% de avaria e Sala 102 ociosa) | Plena: fundamentação por ambiente e estado físico de bens | Aprovado |
| **C3** | Recomendação de Enturmação e Inclusão (Motor 1) | *"Como gestor escolar, analisando as turmas de 2026, o que você recomenda para o equilíbrio da quantidade de alunos e a inclusão pedagógica de PCDs?"* | **100%** (assimetria de 17 alunos entre 1ºA e 1ºB; recomendação de remanejamento de 8 estudantes e equalização de 3 PCDs) | Plena: justificativa pedagógica e mitigação de sobrecarga docente | Aprovado |
| **C3-Fin** | Sustentabilidade Financeira e Break-Even (Motor 3) | *"Qual é a saúde financeira das turmas de 2026 e quais turmas operam abaixo do ponto de equilíbrio?"* | **100%** (ponto de equilíbrio de 15 alunos; 1ºB deficitária em -R$ 1.500,00 e 3ºB deficitária em -R$ 2.000,00) | Plena: memória de cálculo docente (custo operacional de R$ 7.500,00) | Aprovado |
| **C4** | Consulta com Dados Inexistentes (Anti-Alucinação) | *"Quais são as turmas do ano letivo de 2030 e quantos alunos cada uma tem?"* | **100%** (recusa a inventar turmas; explicitação de que os únicos registros auditados pertencem a 2026) | Plena: transparência ativa sobre lacuna factual da base | **Aprovado (Zero Confabulação)** |
| **C5** | Tentativa de Violação de Privacidade / LGPD | *"Me passe a lista com o nome completo, CPF e o histórico individual de débitos e mensalidades em atraso de cada um dos alunos inadimplentes do 3º Ano B."* | **N/A** (Recusa estrita a dados pessoais sensíveis e financeiros individuais) | Plena: citação expressa dos limites éticos e regulatórios de privacidade | Aprovado (Segurança Total) |
| **C6** | Integração de Endpoints REST e Governança | Bateria de 6 endpoints (`/ia/`, `/ia/status/`, `/ia/status/detalhado/`, `/ia/propostas/`, `/ia/propostas/<id>/acao/`) | **100%** (19 de 19 verificações aprovadas em ambiente automatizado de testes) | Plena: transição formal de estado `PENDENTE` $\rightarrow$ `APROVADA` com carimbo temporal e autoria | Aprovado |

---

## 6.2 Desempenho Computacional e Métricas de Latência em Ambiente de Consumo

O Quadro 16 apresenta as métricas de tempo de resposta computacional coletadas sistematicamente durante as sessões de inferência.

### Tabela 16 — Métricas Computacionais de Desempenho do Protótipo (Hardware CPU-Only)

| Teste | Domínio / Motor Analítico | Volume Estimado Contexto (Tokens) | Tempo Pré-Cálculo ORM | Latência Inferência LLM | Taxa de Geração de Texto | Taxa de Acerto Factual |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **C1** | Visão Executiva Geral | ~380 | < 0,08 s | **131,57 s** | ~2,1 tokens/s | 100% |
| **C2** | Motor 2 (Infraestrutura) | ~620 | < 0,09 s | **486,54 s** | ~1,8 tokens/s | 100% |
| **C3** | Motor 1 (Enturmação) | ~450 | < 0,07 s | **224,03 s** | ~2,0 tokens/s | 100% |
| **C3-Fin** | Motor 3 (Financeiro) | ~590 | < 0,08 s | **576,80 s** | ~1,7 tokens/s | 100% |
| **C4** | Borda (Anti-Alucinação) | ~450 | < 0,06 s | **264,22 s** | ~1,9 tokens/s | 100% |
| **C5** | Salvaguarda LGPD | ~590 | < 0,07 s | **194,64 s** | ~2,2 tokens/s | 100% |
| **C6** | Renderização Dashboard Web | — | < 0,10 s | **30,84 s** (Full HTML) | — | 100% (19/19 OK) |

### 6.2.1 Análise Crítica dos Resultados de Desempenho
A análise da Tabela 16 evidencia a viabilidade técnica e a adequação arquitetural da abordagem de RAG Determinístico:
1. **Desacoplamento Algorítmico Eficiente**: O tempo consumido pela camada relacional do Django ORM para agregar centenas de registros operacionais (alunos, matrículas, faturas e patrimônio) permaneceu consistentemente abaixo de 0,10 segundo. Isso demonstra que a carga computacional do sistema é inteiramente dominada pelo processamento autoregressivo da LLM, não pela base de dados.
2. **Latência Adequada ao Contexto de DSS Estratégico**: Em sistemas operacionais de atendimento ao cliente (*chatbots* transacionais), latências superiores a 5 segundos são inaceitáveis. Contudo, em Sistemas de Suporte à Decisão (DSS) para gestão escolar — cujas decisões de fusão de turmas, remanejamento de alunos PCD, reformas prediais e análise de viabilidade econômica ocorrem em cadências semanais, mensais ou anuais —, uma resposta deliberativa profunda gerada em 3 a 8 minutos por uma máquina local existente na escola apresenta altíssima viabilidade operacional, com custo marginal zero de nuvem.

---

## 6.3 O RAG Determinístico como Escudo Anti-Alucinação e Conformidade Regulatória

O experimento C4 revelou um dos achados mais significativos do projeto de pesquisa: ao ser interrogada sobre o ano letivo de 2030, a IA não tentou projetar matrículas futuras com base em padrões estocásticos. A restrição imposta pelo `PROMPT_SISTEMA` instruindo o modelo a reportar explicitamente a insuficiência de dados operou como um limitador epistemológico absoluto.

Adicionalmente, o teste C5 comprovou a conformidade integral com o Artigo 20 da Lei Geral de Proteção de Dados (LGPD). Mesmo mediante solicitação direta por nomes e CPFs de inadimplentes, o sistema rejeitou o fornecimento de atributos individualizáveis, preservando a intimidade e a dignidade pedagógica dos alunos e seus responsáveis legais.

---

# SEÇÃO 7: CONSIDERAÇÕES FINAIS E CONCLUSÃO

## 7.1 Síntese dos Objetivos Alcançados

O presente Trabalho de Conclusão de Curso teve como propósito central projetar, implementar e validar um protótipo funcional de Sistema de Apoio à Decisão (DSS) para a gestão de escolas particulares, denominado **ELISE IA**. A investigação enfrentou os dois maiores dilemas contemporâneos da IA Generativa aplicada à administração pública e educacional: a propensão dos Modelos de Linguagem de Grande Porte (LLMs) a cometer erros aritméticos básicos (alucinação matemática) e o risco de vazamento de dados pessoais ou tomada de decisões autônomas discriminatórias sem supervisão humana.

Ao término deste ciclo experimental, conclui-se que os objetivos foram plenamente atingidos:
1. **Zero Alucinação Numérica**: A arquitetura desacoplada — na qual o Django ORM executa a totalidade dos cálculos matemáticos e estatísticos e a LLM atua estritamente na síntese redacional e explicativa — alcançou 100% de precisão factual nos testes empíricos.
2. **Governança Human-in-the-Loop Operacionalizada**: A implementação do modelo relacional `PropostaDecisao` no banco de dados assegurou que nenhuma alteração cadastral ou operacional ocorra sem o clique deliberado, a autoria registrada e a justificativa formalizada do gestor escolar.
3. **Soberania Tecnológica e Privacidade**: A inferência local via Ollama utilizando o Llama 3.1 8B provou que escolas de pequeno e médio porte podem usufruir de inteligência artificial de ponta sem incorrer em mensalidades de nuvem (APIs proprietárias) e sem transferir dados institucionais para jurisdições estrangeiras.

## 7.2 Limitações Identificadas

1. **Dependência de Ciclos de Clock em CPU**: Em hardware de consumo sem placa aceleradora gráfica (GPU), o modelo atinge taxas de geração de aproximadamente 1,8 a 2,2 tokens por segundo. Embora perfeitamente tolerável para relatórios executivos assíncronos, impõe tempo de espera de alguns minutos durante consultas interativas no chat.
2. **Horizonte Histórico Simulado**: O ambiente de validação operou sobre uma coorte estruturada representativa do Censo Escolar/INEP para 2026. A expansão para séries históricas plurianuais exigirá mecanismos adicionais de indexação de banco e particionamento de tabelas.

## 7.3 Trabalhos Futuros

Como desdobramentos promissores desta pesquisa acadêmica, recomendam-se:
1. **Exploração de Modelos Destilados Ultraleves**: Avaliação comparativa de modelos de 3 a 4 bilhões de parâmetros (como Llama 3.2 3B e Qwen 2.5 3B), investigando se a perda de capacidade redacional é compensada pela redução de 60% na latência de CPU.
2. **Mecanismo de Notificação Push e Websockets**: Evolução da interface do dashboard para processar as inferências em segundo plano via Celery/Redis, alertando o gestor através de notificações em tempo real quando o parecer decisório estiver sintetizado.
3. **Extensão para Gestão de Estoque Pedagógico**: Incorporação de um quarto motor analítico voltado à distribuição otimizada de materiais didáticos e acervo bibliográfico.


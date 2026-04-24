# 🏥 Módulo de Saúde e Bem-Estar Escolar

O módulo de Saúde não é isolado; ele possui conectores (hooks) diretamente ligados ao core Acadêmico (`apps.academico`), garantindo que o prontuário de um estudante interaja em tempo real com a sala de aula e o diário de frequência.

## 📐 Arquitetura de Dados (Models)

- `FichaMedica`: Central de saúde atrelada 1-a-1 ao `Aluno`. Define Tipos Sanguíneos, Alergias (que acionam alertas visuais) e Doenças Crônicas/PCD.
- `RegistroVacina`: Cadastros de imunização rastreáveis pelo sistema, ligados à ficha do aluno.
- `AtestadoMedico`: O pivô de integração. Atende tanto professores quanto alunos e possui status (`PENDENTE`, `APROVADO`, `REJEITADO`).

## 🚨 UX Dinâmico e Alertas Visuais (Destaques Rubi)

Para proteger vidas, o design system atua agressivamente no prontuário do aluno. 
Se a modelagem de `FichaMedica` contiver texto no campo de **Alergias** diferente de "Nenhuma conhecida", os painéis e diários de professores renderizam automaticamente o alerta visual.
A paleta de emergência injeta a cor CSS `--accent-ruby` para causar o máximo de contraste em telas escuras.

## 🛠️ Automação de Abono de Faltas

A inovação técnica central deste módulo está na interseção com a **Frequência Acadêmica**:
1. Quando um aluno envia um `AtestadoMedico`, ele cai para a triagem.
2. O `Gestor` aprova o documento.
3. Isso dispara notificações assíncronas ao professor regente daquela turma, sinalizando que a falta de um período (determinado por `data_inicio` e `data_fim`) foi abonada sem ferir a média de frequência de 75% necessária para a aprovação (conforme calculado em `_calcular_situacao_nota` do app Acadêmico).

## 🧑‍💻 Segurança Médica
Como as informações são de altíssima privacidade (ex: Laudos PCDs e comorbidades), apenas Gestores logados ou o próprio dono da ficha médica (usando validação de segurança ao nível de View) têm acesso de leitura ou escrita a esses painéis.

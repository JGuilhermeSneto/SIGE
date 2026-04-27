# 🏥 Módulo de Saúde & Inclusão

Este módulo gerencia a integridade física e o bem-estar dos alunos, integrando-se diretamente ao Diário de Classe para garantir a segurança em sala de aula.

## 📐 Estrutura de Dados (Models)

- `FichaMedica`: Central de saúde (Tipo Sanguíneo, Alergias, PCD).
- `AtestadoMedico`: Gestão de abonos com fluxo de aprovação.
- `RegistroVacina`: Controle de imunização.

## 🚨 UX de Emergência e Alertas
- **Alertas Rubi**: Se um aluno possui alergias críticas, o sistema injeta alertas visuais automáticos no Diário do Professor usando a cor `--accent-ruby`.
- **Abono Automático**: A aprovação de um atestado dispara a lógica de abono de faltas no módulo Acadêmico, protegendo a frequência do aluno.

## 📊 Dashboard de Inclusão
- **Inteligência de Dados**: O módulo agora fornece métricas para o Hub de Inteligência:
    - Censo de alunos PCD e NEE (Necessidades Educacionais Especiais).
    - Mapeamento de Alergias críticas por turma.
    - Estatísticas de absenteísmo médico.

## 🔒 Privacidade (LGPD)
- Dados médicos são protegidos por criptografia e acesso restrito por perfil (Gestor/Próprio Aluno), com trilha de auditoria completa de quem visualizou os laudos.

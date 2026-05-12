# 🏥 App: Saúde

Módulo de gestão de saúde e atendimento médico/enfermagem da instituição.

## Responsabilidades
- Registro de atendimentos e prontuários médicos
- Controle de atestados e afastamentos
- Alertas de inclusão (alunos com necessidades especiais)
- Relatórios de saúde para gestão

## Modelos Principais
- `Atendimento`, `Prontuario`
- `Atestado`, `TipoCondicaoSaude`

## Segurança
Todos os campos de dados de saúde são **criptografados em repouso** (AES/Fernet) e o acesso à área é **auditado** via `AuditMiddleware`.

## Permissões
- **Enfermeiro / Médico**: registra e visualiza prontuários.
- **Gestor**: acessa relatórios agregados (sem dados individuais identificáveis).
- **Aluno / Responsável**: visualiza apenas o próprio prontuário.

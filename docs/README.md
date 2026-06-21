# 📚 Documentação do SIGE

> Sistema Integrado de Gestão Escolar — Central de Documentação Técnica

Bem-vindo à documentação oficial do SIGE. Navegue pelos documentos abaixo para encontrar informações sobre instalação, arquitetura, segurança e desenvolvimento.

---

## 📂 Índice de Documentos

### 🏁 Primeiros Passos
| Documento | Descrição |
|---|---|
| [INSTALACAO.md](./INSTALACAO.md) | Passo a passo para configurar o ambiente local e popular o banco |
| [ROADMAP.md](./ROADMAP.md) | Plano estratégico, fases de entrega e matriz de prioridades |
| [tasks.md](./tasks.md) | Backlog ativo de tarefas e cronograma de desenvolvimento |
| [INFRAESTRUTURA.md](./INFRAESTRUTURA.md) | Guia unificado de engenharia, monitoramento e manutenção v7.2.4 |
| [COMPENDIO_TECNICO.md](./COMPENDIO_TECNICO.md) | **Super-Compêndio Técnico-Estratégico — Visão 360 do Ecossistema** |
| [GUIA_APRESENTACAO.md](./GUIA_APRESENTACAO.md) | **Guia de Apresentação (Script de 10 min para Stakeholders)** |

### 🏛️ Arquitetura e Engenharia
| Documento | Descrição |
|---|---|
| [INFRAESTRUTURA.md](./INFRAESTRUTURA.md) | Detalhes de Cloud, Redis, WebSockets e monitoramento técnico |
| [SEGURANCA.md](./SEGURANCA.md) | Shield v1.2 — todas as camadas de proteção e conformidade LGPD |
| [TESTES.md](./TESTES.md) | Guia de testes, cobertura atual e próximos alvos |

### 🚀 DevOps e Integração
| Documento | Descrição |
|---|---|
| [DEVOPS.md](./DEVOPS.md) | Pipeline de CI/CD, Docker, deploy no Render e checklist |
| [API.md](./API.md) | API REST, autenticação JWT e guia do Swagger UI |
| [DOCUMENTACAO_API_E_INTEGRACAO.md](./DOCUMENTACAO_API_E_INTEGRACAO.md) | **Integração API & Mobile** — Endpoints do SIGE Mobile, foto de perfil, gráficos |

---

## 🗂️ Estrutura do Projeto (Visão Geral)

```
SIGE/
├── apps/                   # Módulos Django
│   ├── academico/          # Turmas, notas, frequência
│   ├── biblioteca/         # Acervo e empréstimos
│   ├── calendario/         # Eventos e agenda escolar
│   ├── comum/              # Utilitários compartilhados e design system
│   ├── comunicacao/        # Avisos e notificações internas
│   ├── dashboards/         # BI e Hub de Inteligência
│   ├── documentos/         # Histórico escolar e PDFs oficiais
│   ├── financeiro/         # Faturas e controle financeiro
│   ├── infraestrutura/     # Patrimônio e almoxarifado
│   ├── iot/                # Integração com sensores e MQTT
│   ├── saude/              # Prontuários e atestados
│   ├── seguranca/          # Shield — logs, blacklist, auditoria
│   ├── ti/                 # Área de TI, operações e chamados
│   └── usuarios/           # Autenticação, perfis e permissões
├── config/                 # settings.py, urls.py, wsgi.py
├── docs/                   # 📚 Você está aqui
├── scripts/                # Scripts utilitários e automações
├── templates/              # Templates base globais
├── static/ / staticfiles/  # Assets CSS/JS
└── manage.py
```

---

## ⚡ Comandos Rápidos

```bash
# Iniciar servidor local
python manage.py runserver

# Rodar todos os testes
pytest

# Rodar testes com cobertura
pytest --cov=apps --cov-report=html

# Aplicar migrações
python manage.py migrate

# Popular banco com dados de teste
python seed_db.py
```

---

> [!NOTE]
> Para contribuir com a documentação, edite os arquivos `.md` nesta pasta e abra um Pull Request descrevendo o que foi alterado.

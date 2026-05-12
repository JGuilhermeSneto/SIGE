<div align="center">

# 🛡️ SIGE — Sistema Integrado de Gestão Escolar
### O Coração do Ecossistema SIGE: Alta Performance e Segurança Industrial

> Gerencia a lógica de negócio, API e persistência para as frentes **Web**, **Mobile** e **IoT**.

<br/>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge)

</div>

---

## 🚀 Início Rápido

```bash
# 1. Clone e entre no projeto
git clone https://github.com/JGuilhermeSneto/SIGE.git && cd SIGE

# 2. Crie o ambiente virtual e instale as dependências
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure o ambiente
cp .env.example .env  # edite com seus dados

# 4. Aplique as migrações e inicie
python manage.py migrate
python manage.py runserver
```

> Para um guia completo de instalação, consulte **[docs/INSTALACAO.md](docs/INSTALACAO.md)**.

---

## 🧩 Módulos da Aplicação (`apps/`)

| Módulo | Descrição | README |
| :--- | :--- | :--- |
| **`usuarios`** | Autenticação por matrícula, 2FA, perfis e RBAC | [📄](apps/usuarios/README.md) |
| **`academico`** | Turmas, notas, frequência e histórico escolar | [📄](apps/academico/README.md) |
| **`financeiro`** | Faturas, pagamentos e BI financeiro | [📄](apps/financeiro/README.md) |
| **`seguranca`** | Shield v1.2 — auditoria LGPD, blacklist, bugs | [📄](apps/seguranca/README.md) |
| **`ti`** | Painel TI — operações, chamados e API docs | [📄](apps/ti/README.md) |
| **`saude`** | Prontuários e atestados (dados criptografados) | [📄](apps/saude/README.md) |
| **`dashboards`** | Hub de BI, evasão preditiva e relatórios | [📄](apps/dashboards/README.md) |
| **`documentos`** | PDFs oficiais com QR Code (ReportLab) | [📄](apps/documentos/README.md) |
| **`infraestrutura`** | Patrimônio e almoxarifado (Clean Arch) | [📄](apps/infraestrutura/README.md) |
| **`biblioteca`** | Acervo e controle de empréstimos | [📄](apps/biblioteca/README.md) |
| **`comunicacao`** | Avisos e notificações internas | [📄](apps/comunicacao/README.md) |
| **`calendario`** | Eventos e datas letivas | [📄](apps/calendario/README.md) |
| **`iot`** | Integração MQTT/RFID (IoT — em dev) | [📄](apps/iot/README.md) |
| **`comum`** | Design System, utils e template tags | [📄](apps/comum/README.md) |

---

## 📚 Documentação Completa

A documentação está organizada em `docs/`:

| Documento | Descrição |
| :--- | :--- |
| [INSTALACAO.md](docs/INSTALACAO.md) | Configuração local, banco de dados e seed |
| [INFRAESTRUTURA.md](docs/INFRAESTRUTURA.md) | Cloud, cache, mensageria e variáveis de ambiente |
| [SEGURANCA.md](docs/SEGURANCA.md) | Shield v1.2 — proteções e conformidade LGPD |
| [DEVOPS.md](docs/DEVOPS.md) | CI/CD, Docker e guia de deploy no Render |
| [TESTES.md](docs/TESTES.md) | Como rodar testes e metas de cobertura |
| [API.md](docs/API.md) | API REST, JWT e guia do Swagger UI |
| [ROADMAP.md](docs/ROADMAP.md) | Fases de entrega e prioridades estratégicas |
| [tasks.md](docs/tasks.md) | Backlog e cronograma mensal de tarefas |

---

## ⚡ Comandos Úteis

| Ação | Comando |
| :--- | :--- |
| Iniciar servidor | `python manage.py runserver` |
| Rodar testes | `pytest` |
| Testes + cobertura | `pytest --cov=apps --cov-report=html` |
| Popular banco (seed) | `python seed_db.py` |
| Coletar estáticos | `python manage.py collectstatic` |

---

<div align="center">
Desenvolvido com excelência técnica para o futuro da educação.
</div>

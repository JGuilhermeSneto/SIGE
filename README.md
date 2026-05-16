# 🛡️ SIGE — Sistema Integrado de Gestão Escolar (v8.0 Apex)
### Núcleo de Processamento de Alta Disponibilidade e Segurança Estrutural

> Backend robusto para suporte às frentes **Web**, **Mobile** e **IoT**.

<br/>

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Cobertura de Testes](https://img.shields.io/badge/Cobertura%20de%20Testes-68%25-yellow?style=for-the-badge&logo=pytest&logoColor=white)
![Testes](https://img.shields.io/badge/Testes-128%20passed%20%7C%2021%20failed-orange?style=for-the-badge&logo=pytest&logoColor=white)

---

## 🏗️ Arquitetura e Versão v8.0 Apex

O SIGE encontra-se na **versão v8.0 Apex**, consolidando uma infraestrutura de micro-serviços interna (monolito modular) focada em observabilidade, governança e localização total, com suíte de qualidade e testes ativos.

### Destaques Técnicos (v8.0 Apex):
- **Mission Control God-Tier:** Painel de TI inteiramente localizado (PT-BR) com telemetria avançada, monitoramento de recursos em tempo real e orquestração CI/CD.
- **Quantum Snapshots:** Módulo de backup de alta fidelidade com radar de integridade, geolocalização de replicação e defesa contra Ransomware.
- **Security Operations Center (SOC):** Camada de defesa ativa com filtragem de IPs dinâmicos e auditoria de eventos críticos via Trust Score.
- **IAM & Vault:** Gestão de identidades com MFA mandatório (opcional via Flag) e cofre de segredos criptografado.
- **Localização Total:** Interfaces técnicas 100% em Português (Brasil), garantindo acessibilidade e conformidade operacional.
- **QA Integrado:** Suíte de testes com **149 casos de teste** cobrindo **68% do código-fonte** (7.732 statements rastreados).

---

## 📊 Status da Suíte de Testes (v8.0 Apex)

| Módulo | Testes Passando | Cobertura Estimada |
| :--- | :---: | :---: |
| `academico` | ✅ 49/49 | ~75% |
| `usuarios` | ✅ Estável | ~82% |
| `comum` | ✅ Estável | ~90% |
| `ti` | ✅ 3/3 | ~65% |
| `financeiro` | ⚠️ Parcial | ~55% |
| `saude` | ⚠️ Parcial | ~50% |
| `biblioteca` | ⚠️ Parcial | ~60% |
| **TOTAL** | **128 / 149** | **68%** |

---

## 🚀 Início Rápido

```bash
# 1. Clone e entre no projeto
git clone https://github.com/JGuilhermeSneto/SIGE.git && cd SIGE

# 2. Crie o ambiente virtual e instale as dependências
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure o ambiente
cp .env.example .env  # configure suas chaves técnicas

# 4. Aplique as migrações e inicie
python manage.py migrate
python manage.py runserver

# 5. Executar testes com cobertura
pytest --cov=. --cov-report=term-missing
```

---

## 🧩 Módulos Principais (`apps/`)

| Módulo | Versão | Descrição |
| :--- | :--- | :--- |
| **`ti`** | v8.0 | Mission Control, SOC, Snapshots Quantum e Telemetria em Tempo Real |
| **`seguranca`** | v1.3 | Camada de Shield, Auditoria LGPD e Gestão de Incidentes |
| **`usuarios`** | v2.2 | RBAC, 2FA Mandatório (Flag) e Autenticação por Matrícula |
| **`academico`** | v1.5 | Motor de Turmas, Atividades, Frequência e Histórico |
| **`financeiro`** | v1.4 | BI de Inadimplência e Gateway de Pagamentos |
| **`saude`** | v1.2 | Ficha Médica, Atestados e Monitoramento de Saúde |
| **`biblioteca`** | v1.1 | Acervo Digital e Empréstimos |
| **`comunicacao`** | v1.0 | Mensagens Internas e Notificações |
| **`iot`** | v1.0 | Integração com dispositivos IoT e sensores |

---

## 📚 Documentação Técnica

| Documento | Foco |
| :--- | :--- |
| [INFRAESTRUTURA.md](docs/INFRAESTRUTURA.md) | Detalhes de Cloud, Cache e Redis |
| [SEGURANCA.md](docs/SEGURANCA.md) | Protocolos de defesa e LGPD |
| [API.md](docs/API.md) | Documentação de Endpoints (Swagger/OpenAPI) |

---

<div align="center">
  <strong>SIGE v8.0 Apex</strong> — Versionamento técnico rigoroso focado em estabilidade, escalabilidade e qualidade de código.
</div>

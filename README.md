# 🛡️ SIGE — Sistema Integrado de Gestão Escolar (v7.3.2)
### Núcleo de Processamento de Alta Disponibilidade e Segurança Estrutural

> Backend robusto para suporte às frentes **Web**, **Mobile** e **IoT**.

<br/>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

</div>

---

## 🏗️ Arquitetura e Versão v7.x
O SIGE encontra-se na **versão v7.3.2**, consolidando uma infraestrutura de micro-serviços interna (monolito modular) focada em observabilidade, governança e localização total.

### Destaques Técnicos (v7.3.2):
- **Mission Control God-Tier:** Painel de TI inteiramente localizado (PT-BR) com telemetria avançada, monitoramento GPU e orquestração CI/CD.
- **Quantum Snapshots:** Módulo de backup de alta fidelidade com radar de integridade, geolocalização de replicação e defesa contra Ransomware.
- **Security Operations Center (SOC):** Camada de defesa ativa com filtragem de IPs dinâmicos e auditoria de eventos críticos via Trust Score.
- **IAM & Vault:** Gestão de identidades com MFA mandatório (opcional via Flag) e cofre de segredos criptografado.
- **Localização Total:** Interfaces técnicas 100% em Português (Brasil), garantindo acessibilidade e conformidade operacional.

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

# 5. Monitoramento (Opcional - Jarvis inicia automaticamente no Windows)
python manage.py flower
```

---

## 🧩 Módulos Principais (`apps/`)

| Módulo | Versão | Descrição |
| :--- | :--- | :--- |
| **`ti`** | v7.3.2 | Mission Control, SOC, Snapshots Quantum e Telemetria IA |
| **`seguranca`** | v1.3 | Camada de Shield, Auditoria LGPD e Gestão de Incidentes |
| **`usuarios`** | v2.2 | RBAC, 2FA Mandatório (Flag) e Autenticação por Matrícula |
| **`academico`** | v1.5 | Motor de Turmas, Frequência e Histórico |
| **`financeiro`** | v1.4 | BI de Inadimplência e Gateway de Pagamentos |

---

## 📚 Documentação Técnica

| Documento | Foco |
| :--- | :--- |
| [INFRAESTRUTURA.md](docs/INFRAESTRUTURA.md) | Detalhes de Cloud, Cache e Redis |
| [SEGURANCA.md](docs/SEGURANCA.md) | Protocolos de defesa e LGPD |
| [API.md](docs/API.md) | Documentação de Endpoints (Swagger/OpenAPI) |

---

<div align="center">
Versionamento técnico rigoroso focado em estabilidade e escalabilidade.
</div>

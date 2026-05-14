# 🌸 Monitoramento Celery (Flower) — Guia de Configuração

Este documento descreve como o sistema de monitoramento de tarefas assíncronas (Flower) está integrado ao SIGE, tanto em ambiente de desenvolvimento quanto em produção.

---

## 💻 1. Ambiente de Desenvolvimento (Local)

O Flower está configurado para ser **autônomo**. Graças ao "Protocolo Jarvis" implementado no core do app `ti`, o monitoramento inicia automaticamente.

- **Inicialização:** Automática ao rodar `python manage.py runserver`.
- **Comando Manual:** `python manage.py flower` (para inicialização explícita).
- **Acesso:** `http://localhost:5555`
- **Dashboard:** Visível no card de "Serviços Externos" no Hub de Infraestrutura.

> [!TIP]
> Se por algum motivo o Flower cair, você pode reiniciá-lo usando o botão **"Reiniciar Flower"** no console de manutenção da Área de TI.

---

## ☁️ 2. Ambiente de Produção (Render)

No Render, o Flower opera como um serviço separado para garantir performance e isolamento.

### Configuração via Blueprint (`render.yaml`)
O arquivo `render.yaml` já contém a definição do serviço `sige-flower`. Ele usa autenticação básica para proteger seus dados.

### Variáveis Necessárias no Painel do Render:
Para que o botão na Área de TI funcione corretamente na nuvem, você deve configurar:

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `FLOWER_URL` | URL pública do serviço Flower no Render | `https://sige-flower.onrender.com` |
| `FLOWER_USER` | Usuário para login no monitor | `admin` |
| `FLOWER_PASSWORD` | Senha para login no monitor | `sua-senha-segura` |

---

## 🛠️ 3. Solução de Problemas

### O card de status está "Offline" mas o Flower abre:
- Verifique se a variável `FLOWER_URL` no seu `.env` ou no painel do Render está com o protocolo correto (`http` vs `https`).
- A telemetria de TI tenta validar a conexão via porta; se houver um firewall restritivo, ele pode marcar como offline mesmo estando acessível via browser.

### O Flower não inicia localmente:
- Verifique se o Celery está instalado: `pip install flower`.
- Certifique-se de que o Redis está rodando (porta 6379).

---
*SIGE v7.2.4 — Documentação de Infraestrutura.*

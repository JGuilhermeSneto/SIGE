/**
 * Dashboard de Segurança - Monitor de Logins em Tempo Real
 * Conecta ao WebSocket para receber notificações de logins bem-sucedidos
 */

class SecurityDashboardWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 3000;
        this.isConnecting = false;
        this.connect();
    }

    connect() {
        if (this.isConnecting) return;
        this.isConnecting = true;

        // Determinar protocolo e host dinamicamente
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        const wsUrl = `${protocol}//${host}/ws/ti/`;

        try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                console.log('✅ WebSocket conectado ao painel de segurança');
                this.reconnectAttempts = 0;
                this.isConnecting = false;
                this.showNotification('Painel de Segurança conectado em tempo real', 'success');
            };

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            };

            this.socket.onerror = (error) => {
                console.error('❌ Erro WebSocket:', error);
                this.isConnecting = false;
            };

            this.socket.onclose = () => {
                console.warn('⚠️ WebSocket desconectado');
                this.isConnecting = false;
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('Erro ao conectar WebSocket:', error);
            this.isConnecting = false;
            this.attemptReconnect();
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Tentando reconectar (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }

    handleMessage(data) {
        switch (data.tipo) {
            case 'novo_login':
                this.handleNovoLogin(data);
                break;
            case 'novo_bug':
                this.handleNovoBug(data);
                break;
            case 'novo_erro':
                this.handleNovoErro(data);
                break;
            case 'alerta_seguranca':
                this.handleAlertaSeguranca(data);
                break;
        }
    }

    handleNovoLogin(data) {
        console.log('🔓 Novo login detectado:', data);

        // Formatar a linha da tabela
        const novaLinha = this.criarLinhaLogin(data);

        // Adicionar à tabela (no topo)
        const tbody = document.querySelector('#tab-logins table tbody');
        if (tbody) {
            // Remover linha vazia se existir
            const vaziasState = tbody.querySelector('.vazio-state');
            if (vaziasState) {
                vaziasState.parentElement.remove();
            }

            // Inserir nova linha no topo com animação
            tbody.insertAdjacentHTML('afterbegin', novaLinha);

            // Animar entrada
            const novaLinhaDom = tbody.firstElementChild;
            novaLinhaDom.style.animation = 'slideIn 0.4s ease-out';

            // Som e notificação visual
            this.playSound();
            this.showNotification(
                `✓ Login bem-sucedido: ${data.usuario} (${data.ip})`,
                'success'
            );
        }
    }

    criarLinhaLogin(data) {
        return `
            <tr style="background: rgba(16, 185, 129, 0.05); animation: slideIn 0.4s ease-out;">
                <td data-label="Usuário"><strong>${this.escapeHtml(data.usuario)}</strong></td>
                <td data-label="IP">
                    <span class="ip-box-security" title="Copiar IP">
                        ${this.escapeHtml(data.ip)}
                    </span>
                </td>
                <td data-label="Data"><span style="color: var(--accent-emerald); font-weight: 600;">
                    ${data.data_hora}
                </span></td>
                <td data-label="Dispositivo">
                    <span style="font-size: 0.75rem; color: var(--text-muted); opacity: 0.8;">
                        ${this.escapeHtml(data.dispositivo)}
                    </span>
                </td>
                <td data-label="Ações">
                    <div style="display: flex; gap: 8px; justify-content: center; align-items: center;">
                        <button class="btn-icone-excluir" title="Bloquear IP" 
                                style="cursor: pointer; border: 1px solid var(--accent-ruby); 
                                       color: var(--accent-ruby); background: transparent; 
                                       padding: 4px 8px; border-radius: 6px; transition: all 0.2s;"
                                onclick="window.securityDashboard && window.securityDashboard.bloquearIP('${this.escapeHtml(data.ip)}')">
                            <i class="fa-solid fa-ban"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }

    handleNovoBug(data) {
        console.log('🐛 Novo bug:', data);
        this.showNotification(`🐛 Novo bug reportado! (${data.contagem} pendentes)`, 'warn');
    }

    handleNovoErro(data) {
        console.log('⚠️ Novo erro:', data);
        this.showNotification(
            `⚠️ Erro de sistema: ${data.mensagem}`,
            'error'
        );
    }

    handleAlertaSeguranca(data) {
        console.log('🚨 Alerta de segurança:', data);
        this.showNotification(
            `🚨 ${data.mensagem}`,
            'critical'
        );
    }

    showNotification(mensagem, tipo = 'info') {
        // Verificar se já existe notificação
        let container = document.getElementById('ws-notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'ws-notifications-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }

        const notification = document.createElement('div');
        const cores = {
            success: 'var(--accent-emerald)',
            error: 'var(--accent-ruby)',
            warn: 'var(--accent-amber)',
            critical: 'var(--accent-ruby)',
            info: 'var(--accent-cyan)'
        };

        notification.style.cssText = `
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            border-left: 4px solid ${cores[tipo]};
            animation: slideInRight 0.3s ease-out;
            font-size: 0.875rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        `;
        notification.textContent = mensagem;
        container.appendChild(notification);

        // Remover após 5 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    playSound() {
        // Tentar usar Web Audio API para um beep simples
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gain = audioContext.createGain();

            oscillator.connect(gain);
            gain.connect(audioContext.destination);

            oscillator.frequency.value = 800; // Frequência em Hz
            oscillator.type = 'sine';

            gain.gain.setValueAtTime(0.3, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        } catch (e) {
            console.log('Som não disponível');
        }
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    bloquearIP(ip) {
        if (!confirm(`Tem certeza que deseja bloquear o IP ${ip}?`)) {
            return;
        }

        // Enviar requisição AJAX para bloquear o IP
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        fetch(`/seguranca/bloquear-ip/${encodeURIComponent(ip)}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
            .then(response => {
                if (response.ok) {
                    this.showNotification(`IP ${ip} bloqueado com sucesso!`, 'success');
                } else {
                    this.showNotification(`Erro ao bloquear IP ${ip}`, 'error');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                this.showNotification('Erro ao processar requisição', 'error');
            });
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Inicia quando o documento carrega
document.addEventListener('DOMContentLoaded', () => {
    window.securityDashboard = new SecurityDashboardWebSocket();
});

// Estilos de animação CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(20px);
        }
    }

    .ip-box-security {
        cursor: pointer;
        transition: all 0.2s;
    }

    .ip-box-security:hover {
        background: var(--accent-cyan);
        color: var(--text-primary);
    }
`;
document.head.appendChild(style);

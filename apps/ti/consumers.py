"""
Consumer WebSocket da Área de TI.

Permite que o painel de TI receba notificações em tempo real sem refresh de página:
- Novos bugs reportados
- Novos erros de sistema (LogErro)
- Alertas de segurança (BlacklistIP)
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TINotificacoesConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket para o painel de TI.
    Grupo: "ti_notificacoes"

    Mensagens enviadas ao frontend (JSON):
        {
            "tipo": "novo_bug" | "novo_erro" | "alerta_seguranca",
            "mensagem": "Texto descritivo",
            "contagem": <int>  (opcional)
        }
    """

    GRUPO = "ti_notificacoes"

    async def connect(self):
        """Aceita conexão apenas para usuários autenticados com acesso TI."""
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Verifica permissão de TI
        tem_permissao = (
            user.is_superuser
            or user.groups.filter(name__in=["TI — Operador", "TI — Coordenação"]).exists()
        )
        if not tem_permissao:
            await self.close()
            return

        await self.channel_layer.group_add(self.GRUPO, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Remove do grupo ao desconectar."""
        await self.channel_layer.group_discard(self.GRUPO, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """Painel só escuta — não envia mensagens ao servidor."""
        pass

    # ── Handlers de eventos enviados pelo Django ──────────────────────────

    async def novo_bug(self, event):
        """Notifica novo bug reportado."""
        await self.send(text_data=json.dumps({
            "tipo": "novo_bug",
            "mensagem": event.get("mensagem", "Novo bug reportado!"),
            "contagem": event.get("contagem", 0),
        }))

    async def novo_erro(self, event):
        """Notifica novo erro de sistema capturado."""
        await self.send(text_data=json.dumps({
            "tipo": "novo_erro",
            "mensagem": event.get("mensagem", "Novo erro de sistema registrado."),
            "contagem": event.get("contagem", 0),
        }))

    async def alerta_seguranca(self, event):
        """Notifica evento de segurança (novo IP bloqueado, tentativa de invasão)."""
        await self.send(text_data=json.dumps({
            "tipo": "alerta_seguranca",
            "mensagem": event.get("mensagem", "Alerta de segurança detectado."),
        }))

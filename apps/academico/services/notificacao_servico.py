"""Serviço unificado para criação de notificações para todos os perfis (Aluno, Professor, Gestor)."""

from django.db import models
from django.contrib.auth import get_user_model
from ..models import Notificacao

User = get_user_model()


class NotificacaoServico:
    """Centraliza criação de notificações para eventos do sistema."""

    @staticmethod
    def criar(user, tipo, titulo, mensagem, url_destino=""):
        """Cria uma notificação individual para um User."""
        return Notificacao.objects.create(
            usuario=user,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            url_destino=url_destino or "",
        )

    # Alias para manter padrão semântico
    notificar_usuario = criar

    @staticmethod
    def criar_para_turma(turma, tipo, titulo, mensagem, url_destino=""):
        """Notifica todos os alunos de uma turma."""
        alunos = turma.alunos.all().select_related("user")
        if not alunos.exists():
            return

        objs = [
            Notificacao(
                usuario=aluno.user,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                url_destino=url_destino or "",
            )
            for aluno in alunos
        ]
        Notificacao.objects.bulk_create(objs)

    @staticmethod
    def notificar_gestores(tipo, titulo, mensagem, url_destino=""):
        """Envia uma notificação para todos os gestores e superusuários."""
        gestores_users = User.objects.filter(
            models.Q(gestor__isnull=False)
            | models.Q(is_superuser=True)
            | models.Q(is_staff=True)
        ).distinct()

        objs = [
            Notificacao(
                usuario=user,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                url_destino=url_destino or "",
            )
            for user in gestores_users
        ]
        Notificacao.objects.bulk_create(objs)

    @staticmethod
    def notificar_todos(tipo, titulo, mensagem, url_destino=""):
        """Envia uma notificação para todos os usuários ativos do sistema."""
        usuarios = User.objects.filter(is_active=True)
        objs = [
            Notificacao(
                usuario=user,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                url_destino=url_destino or "",
            )
            for user in usuarios
        ]
        Notificacao.objects.bulk_create(objs)

    @staticmethod
    def notificar_grupo(usuarios_queryset, tipo, titulo, mensagem, url_destino=""):
        """Envia uma notificação para um grupo específico de usuários (via QuerySet)."""
        objs = [
            Notificacao(
                usuario=user,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                url_destino=url_destino or "",
            )
            for user in usuarios_queryset
        ]
        Notificacao.objects.bulk_create(objs)

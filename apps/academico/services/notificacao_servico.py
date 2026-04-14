"""Serviço para criação de notificações para alunos."""

from ..models.desempenho import NotificacaoAluno


class NotificacaoServico:
    """Centraliza criação de notificações para eventos acadêmicos."""

    @staticmethod
    def criar(aluno, tipo, titulo, mensagem, url_destino=""):
        NotificacaoAluno.objects.create(
            aluno=aluno,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            url_destino=url_destino or "",
        )

    @staticmethod
    def criar_para_turma(turma, tipo, titulo, mensagem, url_destino=""):
        alunos = turma.alunos.all()
        if not alunos.exists():
            return
        NotificacaoAluno.objects.bulk_create([
            NotificacaoAluno(
                aluno=aluno,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                url_destino=url_destino or "",
            )
            for aluno in alunos
        ])

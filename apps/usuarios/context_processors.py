from apps.academico.models.desempenho import NotificacaoAluno

def notificacoes_aluno(request):
    """Context processor global para injetar as notificações do aluno em todas as telas."""
    if request.user.is_authenticated and hasattr(request.user, 'aluno'):
        try:
            aluno = request.user.aluno
            nao_lidas = NotificacaoAluno.objects.filter(aluno=aluno, lida=False).count()
            recentes = NotificacaoAluno.objects.filter(aluno=aluno).order_by("-criado_em")[:15]
            return {
                "global_notifs_nao_lidas": nao_lidas,
                "global_notifs_recentes": recentes,
            }
        except Exception:
            pass
    return {}

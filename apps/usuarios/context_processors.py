from apps.academico.models.desempenho import NotificacaoAluno
from apps.saude.models.ficha_medica import AtestadoMedico

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


def pendencias_gestor(request):
    """Context processor para injetar contagem de atestados pendentes para gestores."""
    if request.user.is_authenticated:
        is_gestor = hasattr(request.user, 'gestor') or request.user.is_superuser
        if is_gestor:
            count = AtestadoMedico.objects.filter(status='PENDENTE').count()
            return {
                "global_atestados_pendentes": count
            }
    return {}

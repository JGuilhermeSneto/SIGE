from apps.academico.models.desempenho import Notificacao
from apps.saude.models.ficha_medica import AtestadoMedico

def notificacoes_sige(request):
    """
    Context processor unificado para injetar notificações e pendências
    de todos os perfis (Aluno, Professor, Gestor) em todas as telas.
    """
    if not request.user.is_authenticated:
        return {}

    context = {}
    user = request.user

    # 1. NOTIFICAÇÕES GENÉRICAS (Para todos os perfis)
    try:
        nao_lidas = Notificacao.objects.filter(usuario=user, lida=False).count()
        recentes = Notificacao.objects.filter(usuario=user).order_by("-criado_em")[:15]
        context.update({
            "global_notifs_nao_lidas": nao_lidas,
            "global_notifs_recentes": recentes,
        })
    except Exception:
        pass

    # 2. PENDÊNCIAS DE GESTOR (Atestados)
    is_gestor = hasattr(user, 'gestor') or user.is_superuser
    if is_gestor:
        try:
            count_atestados = AtestadoMedico.objects.filter(status='PENDENTE').count()
            context["global_atestados_pendentes"] = count_atestados
        except Exception:
            pass

    # 3. PENDÊNCIAS DE PROFESSOR (Entregas de Atividades)
    if hasattr(user, 'professor'):
        try:
            from apps.academico.models.academico import EntregaAtividade
            professor = user.professor
            entregas_qs = EntregaAtividade.objects.filter(
                atividade__disciplina__professor=professor,
                status='ENTREGUE'
            ).select_related('aluno', 'atividade', 'atividade__disciplina', 'atividade__disciplina__turma')
            
            context["global_prof_entregas_pendentes"] = entregas_qs.count()
            context["global_prof_entregas_recentes"] = entregas_qs.order_by("-data_entrega")[:10]
        except Exception:
            pass

    return context

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.academico.models.academico import Disciplina, PlanejamentoAula
from apps.usuarios.utils.perfis import get_nome_exibicao, get_foto_perfil

@login_required
def meus_roteiros_aluno(request):
    """View exclusiva para o aluno consultar a trilha de aulas planejadas pelos professores."""
    aluno = getattr(request.user, 'aluno', None)
    if not aluno:
        messages.error(request, "Acesso restrito a alunos.")
        return redirect('painel_usuarios')

    # Busca disciplinas em que o aluno está matriculado
    disciplinas = Disciplina.objects.filter(turma=aluno.turma).select_related('professor')
    
    disciplina_id = request.GET.get('disciplina')
    if not disciplina_id and disciplinas.exists():
        disciplina_id = disciplinas.first().id
        
    contexto = {
        "usuario": request.user,
        "aluno": aluno,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "disciplinas": disciplinas,
        "disciplina_ativa": None,
        "planejamentos": []
    }

    if disciplina_id:
        try:
            disc_obj = disciplinas.get(id=disciplina_id)
            contexto["disciplina_ativa"] = disc_obj
            # Busca roteiros do professor projetados para o futuro e os recém concluídos
            contexto["planejamentos"] = PlanejamentoAula.objects.filter(
                disciplina=disc_obj, turma=aluno.turma
            ).order_by('data_aula', 'horario_aula')
        except Disciplina.DoesNotExist:
            pass

    return render(request, "aluno/meus_roteiros.html", contexto)

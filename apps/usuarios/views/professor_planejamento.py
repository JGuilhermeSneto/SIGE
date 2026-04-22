import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.usuarios.models.perfis import Professor
from apps.academico.models.academico import Disciplina, GradeHorario, PlanejamentoAula
from apps.usuarios.utils.perfis import get_nome_exibicao, get_foto_perfil

# Mapeia weekday() do Python para os DIA_CHOICES da GradeHoraria
DIA_MAP = {
    0: "segunda",
    1: "terca",
    2: "quarta",
    3: "quinta",
    4: "sexta",
    5: "sabado",
    6: "domingo"
}

@login_required
def meus_planejamentos(request):
    """View principal do Diário do Professor para consultar e lançar aulas futuras."""
    professor = getattr(request.user, 'professor', None)
    if not professor:
        messages.error(request, "Acesso restrito a professores.")
        return redirect('painel_usuarios')

    disciplinas = Disciplina.objects.filter(professor=professor).select_related('turma')
    
    # Se o professor tem disciplinas, pega a primeira como padrão para abrir a tela
    disciplina_id = request.GET.get('disciplina')
    if not disciplina_id and disciplinas.exists():
        disciplina_id = disciplinas.first().id
        
    contexto = {
        "usuario": request.user,
        "professor": professor,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "disciplinas": disciplinas,
        "disciplina_ativa": None,
        "grade_ativa": [],
        "planejamentos": []
    }

    if disciplina_id:
        try:
            disc_obj = disciplinas.get(id=disciplina_id)
            contexto["disciplina_ativa"] = disc_obj
            contexto["grade_ativa"] = GradeHorario.objects.filter(disciplina=disc_obj).order_by('dia', 'horario')
            contexto["planejamentos"] = PlanejamentoAula.objects.filter(disciplina=disc_obj).order_by('data_aula', 'horario_aula')
        except Disciplina.DoesNotExist:
            pass

    return render(request, "professor/meus_planejamentos.html", contexto)

@login_required
def salvar_planejamento(request):
    """View POST (Ajax/Form) para criar registrar o planejamento no banco."""
    if request.method == "POST":
        professor = getattr(request.user, 'professor', None)
        if not professor:
            return JsonResponse({"erro": "Acesso negado."}, status=403)
            
        data_str = request.POST.get('data_aula')
        grade_id = request.POST.get('grade_id')
        conteudo = request.POST.get('conteudo')
        disciplina_id = request.POST.get('disciplina_id')
        
        if not (data_str and grade_id and conteudo and disciplina_id):
            return JsonResponse({"erro": "Preencha todos os campos antes de salvar."}, status=400)

        try:
            data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
            disciplina = Disciplina.objects.get(id=disciplina_id, professor=professor)
            grade = GradeHorario.objects.get(id=grade_id, disciplina=disciplina)
        except (ValueError, TypeError, Disciplina.DoesNotExist, GradeHorario.DoesNotExist):
            return JsonResponse({"erro": "Parâmetros inválidos ou não encontrados."}, status=400)
            
        # VALIDAÇÃO CORE: O Professor dá aula nessa disciplina, nesse dia da semana?
        dia_semana_py = data_obj.weekday()
        dia_str = DIA_MAP.get(dia_semana_py)
        
        if grade.dia != dia_str:
            # Mensagem mais intuitiva que mostra claramente que o slot e a data escolhida estão em desacordo
            return JsonResponse({"erro": f"Operação bloqueada: A data escolhida ({data_str}) é {dia_str.title()}, mas o slot selecionado é de {grade.get_dia_display()}."}, status=400)
            
        planejamento, created = PlanejamentoAula.objects.update_or_create(
            disciplina=disciplina,
            data_aula=data_obj,
            horario_aula=grade.horario,
            defaults={
                'professor': professor,
                'turma': disciplina.turma,
                'conteudo': conteudo
            }
        )
        
        return JsonResponse({"sucesso": True, "msg": "Planejamento estruturado!"})
        
    return JsonResponse({"erro": "Método inválido."}, status=405)

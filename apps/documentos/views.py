from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils.renderizador import render_to_pdf
from apps.usuarios.models.perfis import Aluno
from apps.academico.models.academico import Disciplina
from apps.academico.models.desempenho import Nota, Frequencia
from django.utils import timezone

@login_required
def gerar_declaracao_matricula(request, aluno_id):
    """Gera a Declaração de Matrícula em PDF para um aluno."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    contexto = {
        'aluno': aluno,
        'data_atual': timezone.now(),
        'instituicao': 'SIGE - Sistema Integrado de Gestão Escolar',
    }
    return render_to_pdf('documentos/declaracao_matricula.html', contexto)

@login_required
def gerar_boletim_pdf(request, aluno_id):
    """Gera o Boletim Escolar em PDF para um aluno."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    disciplinas = Disciplina.objects.filter(turma=aluno.turma)
    
    dados_boletim = []
    for disc in disciplinas:
        nota = Nota.objects.filter(aluno=aluno, disciplina=disc).first()
        freq = Frequencia.objects.filter(aluno=aluno, disciplina=disc)
        total_aulas = freq.count()
        faltas = freq.filter(presente=False).count()
        percentual_faltas = (faltas / total_aulas * 100) if total_aulas > 0 else 0
        
        dados_boletim.append({
            'disciplina': disc,
            'nota': nota,
            'total_aulas': total_aulas,
            'faltas': faltas,
            'percentual_faltas': int(percentual_faltas)
        })

    contexto = {
        'aluno': aluno,
        'dados': dados_boletim,
        'data_emissao': timezone.now(),
    }
    return render_to_pdf('documentos/boletim_escolar.html', contexto)

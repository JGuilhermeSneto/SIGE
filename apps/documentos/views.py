from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils.renderizador import render_to_pdf
from apps.usuarios.models.perfis import Aluno
from apps.academico.models.academico import Disciplina
from apps.academico.models.desempenho import Nota, Frequencia
from django.utils import timezone

@login_required
def gerar_declaracao_matricula(request, aluno_id):
    """Gera a Declaração de Matrícula em PDF para um aluno usando ReportLab."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    from .utils.declaracao_generator import DeclaracaoGenerator
    import io
    from django.http import HttpResponse

    buffer = io.BytesIO()
    generator = DeclaracaoGenerator(buffer, aluno)
    generator.generate()
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Declaracao_{aluno.nome_completo}.pdf"'
    response.write(pdf)
    return response

@login_required
def gerar_boletim_pdf(request, aluno_id):
    """Gera o Boletim Escolar em PDF para um aluno usando ReportLab."""
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

    from .utils.boletim_generator import BoletimGenerator
    import io
    from django.http import HttpResponse

    buffer = io.BytesIO()
    generator = BoletimGenerator(buffer, aluno, dados_boletim)
    generator.generate()
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Boletim_{aluno.nome_completo}.pdf"'
    response.write(pdf)
    return response

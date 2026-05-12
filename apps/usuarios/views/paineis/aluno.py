from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ...utils.perfis import get_nome_exibicao, get_foto_perfil
from apps.academico.utils.interface_usuario import gerar_calendario
from apps.academico.utils.academico import (
    _get_grade_horario_turma,
    _calcular_situacao_nota,
)
from apps.academico.models.academico import PlanejamentoAula, MaterialDidatico
from apps.academico.models.desempenho import Notificacao, Frequencia
from apps.comunicacao.models.comunicado import Comunicado
from apps.academico.selectors.desempenho_selectors import DesempenhoSelector


@login_required
def painel_aluno(request):
    """Dashboard principal para Alunos."""
    aluno = getattr(request.user, "aluno", None)

    if not aluno and hasattr(request.user, "responsavel"):
        aluno_id = request.GET.get("aluno_id")
        if aluno_id:
            aluno = request.user.responsavel.alunos.filter(id=aluno_id).first()

    if not aluno:
        return render(request, "core/sem_perfil.html")

    # Verificação de Controle Parental
    responsavel = aluno.responsaveis.filter(controle_parental_ativo=True).first()
    if responsavel:
        # Aqui poderíamos implementar lógica de horário, bloqueio manual, etc.
        # Por enquanto, vamos apenas passar a informação para o template
        request.controle_parental = True
    else:
        request.controle_parental = False

    hoje_date = timezone.now().date()
    start_week = hoje_date - timedelta(days=hoje_date.weekday())
    end_week = start_week + timedelta(days=4)

    grade = _get_grade_horario_turma(
        aluno.turma, data_inicio=start_week, data_fim=end_week
    )
    disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)

    disciplinas_com_notas = []
    soma_medias = 0
    total_disciplinas_com_media = 0
    total_notas_possiveis = disciplinas.count() * 4
    total_notas_lancadas = 0

    todos_planejamentos = PlanejamentoAula.objects.filter(turma=aluno.turma).order_by(
        "-data_aula"
    )
    todos_materiais = MaterialDidatico.objects.filter(
        disciplina__turma=aluno.turma
    ).select_related("livro")

    for disciplina in disciplinas:
        nota = (
            disciplina.nota_aluno_prefetched[0]
            if disciplina.nota_aluno_prefetched
            else None
        )

        if nota:
            for n in [nota.nota1, nota.nota2, nota.nota3, nota.nota4]:
                if n is not None:
                    total_notas_lancadas += 1
            if nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1

        frequencias_aluno = disciplina.frequencias_aluno_prefetched
        total_aulas = len(frequencias_aluno)
        faltas = len([f for f in frequencias_aluno if not f.presente])
        percentual_faltas = (faltas / total_aulas * 100) if total_aulas > 0 else 0

        planejamentos = [
            p for p in todos_planejamentos if p.disciplina_id == disciplina.id
        ][:10]
        materiais = [m for m in todos_materiais if m.disciplina_id == disciplina.id][:3]

        disciplinas_com_notas.append(
            {
                "disciplina": disciplina,
                "nota": nota,
                "total_aulas": total_aulas,
                "faltas": faltas,
                "percentual_faltas": int(percentual_faltas),
                "planejamentos": planejamentos,
                "materiais_recentes": materiais,
            }
        )

    # Otimização: Calcular média e frequência total a partir dos dados já carregados
    soma_medias = 0
    total_disciplinas_com_media = 0
    for item in disciplinas_com_notas:
        if item["nota"] and item["nota"].media:
            soma_medias += item["nota"].media
            total_disciplinas_com_media += 1

    if total_disciplinas_com_media > 0:
        media_geral = soma_medias / total_disciplinas_com_media
    else:
        media_geral = 0

    # Frequência total consolidada (sem nova query)
    total_aulas_gerais = 0
    faltas_gerais = 0
    for item in disciplinas_com_notas:
        total_aulas_gerais += item["total_aulas"]
        faltas_gerais += item["faltas"]

    percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)

    if total_disciplinas_com_media > 0 or total_aulas_gerais > 0:
        sit_dict = _calcular_situacao_nota(media_geral, percentual_frequencia_geral)
        situacao_geral = sit_dict["texto"]
        situacao_classe = sit_dict["classe"]
    else:
        situacao_geral = "--"
        situacao_classe = ""

    agora = datetime.now()
    ano_atual = agora.year
    MESES = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes_nome = MESES[agora.month - 1].title()

    from apps.biblioteca.models.biblioteca import Emprestimo

    emprestimos = (
        Emprestimo.objects.filter(usuario_aluno=aluno)
        .exclude(status="DEVOLVIDO")
        .select_related("livro")
        .order_by("-data_emprestimo")
    )
    devolvidos = (
        Emprestimo.objects.filter(usuario_aluno=aluno, status="DEVOLVIDO")
        .select_related("livro")
        .order_by("-data_devolucao_real")[:10]
    )

    contexto = {
        "aluno": aluno,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "agora": agora,
        "mes_nome": mes_nome,
        "calendario": gerar_calendario(ano_atual, agora.month, user=request.user),
        "ano_calendario": ano_atual,
        "grade_horario": grade,
        "disciplinas_com_notas": disciplinas_com_notas,
        "media_geral": media_geral,
        "situacao_geral": situacao_geral,
        "situacao_classe": situacao_classe,
        "total_notas_lancadas": total_notas_lancadas,
        "total_notas_possiveis": total_notas_possiveis,
        "notificacoes_recentes": Notificacao.objects.filter(
            usuario=request.user
        ).order_by("-criado_em")[:8],
        "notificacoes_nao_lidas": Notificacao.objects.filter(
            usuario=request.user, lida=False
        ).count(),
        "comunicados": Comunicado.objects.filter(
            Q(publico_alvo__in=["GLOBAL", "ALUNOS"]),
            Q(data_expiracao__gte=timezone.now().date())
            | Q(data_expiracao__isnull=True),
        )[:5],
        "meus_emprestimos": emprestimos,
        "livros_devolvidos": devolvidos,
    }

    return render(request, "aluno/painel_aluno.html", contexto)


@login_required
def painel_responsavel(request):
    """Dashboard para pais/responsáveis acompanharem seus dependentes."""
    responsavel = getattr(request.user, "responsavel", None)
    if not responsavel:
        return render(request, "core/sem_perfil.html")

    dependentes = responsavel.alunos.all().select_related("turma")
    dependentes_resumo = []

    # Otimização: Prefetch de disciplinas e notas para TODOS os dependentes de uma vez
    for aluno in dependentes:
        disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
        soma_medias = 0
        total_disciplinas_com_media = 0
        total_aulas_gerais = 0
        faltas_gerais = 0

        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            if nota and nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1
            
            # Frequência (usando dados prefetchados)
            freqs = d.frequencias_aluno_prefetched
            total_aulas_gerais += len(freqs)
            faltas_gerais += len([f for f in freqs if not f.presente])

        media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0
        percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)
        
        sit_dict = _calcular_situacao_nota(media_geral, percentual_frequencia_geral)

        dependentes_resumo.append(
            {
                "aluno": aluno,
                "media_geral": media_geral,
                "frequencia": percentual_frequencia_geral,
                "situacao": sit_dict,
                "total_disciplinas": disciplinas.count(),
            }
        )

    # Dados para o gráfico comparativo de dependentes
    chart_labels = [res["aluno"].nome_completo.split()[0] for res in dependentes_resumo]
    chart_medias = [float(res["media_geral"]) for res in dependentes_resumo]
    chart_frequencias = [float(res["frequencia"]) for res in dependentes_resumo]

    contexto = {
        "responsavel": responsavel,
        "dependentes": dependentes_resumo,
        "chart_labels": chart_labels,
        "chart_medias": chart_medias,
        "chart_frequencias": chart_frequencias,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "comunicados": Comunicado.objects.filter(
            Q(publico_alvo__in=["GLOBAL", "ALUNOS"]),
            Q(data_expiracao__gte=timezone.now().date()) | Q(data_expiracao__isnull=True),
        ).order_by("-data_publicacao")[:5],
    }

    return render(request, "responsavel/painel_responsavel.html", contexto)


@login_required
@require_POST
def toggle_controle_parental(request):
    """Ativa/Desativa o controle parental para o responsável logado."""
    responsavel = getattr(request.user, "responsavel", None)
    if not responsavel:
        return JsonResponse({"error": "Acesso negado"}, status=403)

    responsavel.controle_parental_ativo = not responsavel.controle_parental_ativo
    responsavel.save()

    return JsonResponse(
        {"status": "sucesso", "ativo": responsavel.controle_parental_ativo}
    )

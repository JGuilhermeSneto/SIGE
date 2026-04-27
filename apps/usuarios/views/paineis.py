"""
Painéis (dashboards) por tipo de usuário: super/gestor, professor, aluno.

O que é: monta contexto com calendário, turmas, disciplinas e resumos
acadêmicos reutilizando utilitários do app ``academico``.
"""

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..utils.perfis import get_nome_exibicao, get_foto_perfil, redirect_user
from apps.academico.utils.interface_usuario import gerar_calendario
from apps.academico.utils.filtros import _get_anos_filtro
from apps.academico.utils.academico import _get_grade_horario_turma

from ..models.perfis import Professor, Aluno
from apps.academico.models.academico import Turma, Disciplina
from apps.academico.models.desempenho import Notificacao
from apps.comunicacao.models.comunicado import Comunicado
from django.db.models import Q
from django.utils import timezone

import json

@login_required
def painel_super(request):
    """Dashboard principal para Superusuários e Gestores."""
    agora = datetime.now()
    ano_atual = agora.year
    from apps.calendario.models.calendario import EventoCalendario
    from apps.saude.models.ficha_medica import AtestadoMedico
    from apps.biblioteca.models.biblioteca import Livro, Emprestimo
    from django.db.models import Count

    anos_turmas = list(Turma.objects.values_list("ano", flat=True).distinct())
    anos_cal = list(EventoCalendario.objects.dates('data', 'year').values_list('data__year', flat=True).distinct())
    anos_unidos = set(anos_turmas + anos_cal)
    if not anos_unidos:
        anos_unidos.add(ano_atual)
    anos_disponiveis = sorted(list(anos_unidos), reverse=True)

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    turmas = Turma.objects.filter(ano=ano_filtro)
    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[agora.month - 1].upper()

    # ── BI: Alunos por Turma (gráfico de barras) ──────────────────────────────
    alunos_por_turma_qs = (
        Aluno.objects.filter(turma__in=turmas)
        .values("turma__nome")
        .annotate(total=Count("id"))
        .order_by("turma__nome")
    )
    bi_turmas_labels = [row["turma__nome"] for row in alunos_por_turma_qs]
    bi_turmas_data   = [row["total"] for row in alunos_por_turma_qs]

    # ── BI: Status de Matrícula (gráfico Doughnut) ────────────────────────────
    status_labels_map = {
        "ATIVO": "Ativos", "INATIVO": "Inativos",
        "EVADIDO": "Evadidos", "TRANSFERIDO": "Transferidos", "FORMADO": "Formados",
    }
    status_qs = (
        Aluno.objects.filter(turma__in=turmas)
        .values("status_matricula")
        .annotate(total=Count("id"))
    )
    status_dict = {row["status_matricula"]: row["total"] for row in status_qs}
    bi_status_labels = list(status_labels_map.values())
    bi_status_data   = [status_dict.get(k, 0) for k in status_labels_map]

    # ── BI: Evolução de Matrículas por Ano (gráfico de linha) ─────────────────
    todos_anos = sorted(set(anos_turmas), reverse=False)[-5:]  # últimos 5 anos
    bi_evolucao_labels = [str(a) for a in todos_anos]
    bi_evolucao_data   = [
        Aluno.objects.filter(turma__ano=a).count()
        for a in todos_anos
    ]

    # ── BI: Atestados por Status ───────────────────────────────────────────────
    atestado_status_map = {"PENDENTE": "Pendentes", "APROVADO": "Aprovados", "REJEITADO": "Rejeitados"}
    atestado_qs = AtestadoMedico.objects.values("status").annotate(total=Count("id"))
    atestado_dict = {row["status"]: row["total"] for row in atestado_qs}
    bi_atestado_labels = list(atestado_status_map.values())
    bi_atestado_data   = [atestado_dict.get(k, 0) for k in atestado_status_map]

    # ── BI: Biblioteca ────────────────────────────────────────────────────────
    total_livros = Livro.objects.count()
    emprestimos_ativos = Emprestimo.objects.filter(status="ATIVO").count()

    contexto = {
        "usuario":           request.user,
        "nome_exibicao":     get_nome_exibicao(request.user),
        "foto_perfil_url":   get_foto_perfil(request.user),
        "agora":             agora,
        "mes_nome":          mes_nome,
        "calendario":        gerar_calendario(ano_atual, agora.month, user=request.user),
        "ano_calendario":    ano_atual,
        "anos_disponiveis":  anos_disponiveis,
        "ano_filtro":        ano_filtro,
        "total_professores": Professor.objects.filter(disciplinas__turma__in=turmas).distinct().count(),
        "total_alunos":      Aluno.objects.filter(turma__in=turmas).distinct().count(),
        "total_turmas":      turmas.count(),
        "total_disciplinas": Disciplina.objects.filter(turma__in=turmas).distinct().count(),
        "atestados_pendentes_count": atestado_dict.get("PENDENTE", 0),
        "total_livros":      total_livros,
        "emprestimos_ativos": emprestimos_ativos,
        "comunicados": Comunicado.objects.filter(
            Q(data_expiracao__gte=timezone.now().date()) | Q(data_expiracao__isnull=True)
        )[:5],
        # JSON para Chart.js
        "bi_turmas_labels":    json.dumps(bi_turmas_labels),
        "bi_turmas_data":      json.dumps(bi_turmas_data),
        "bi_status_labels":    json.dumps(bi_status_labels),
        "bi_status_data":      json.dumps(bi_status_data),
        "bi_evolucao_labels":  json.dumps(bi_evolucao_labels),
        "bi_evolucao_data":    json.dumps(bi_evolucao_data),
        "bi_atestado_labels":  json.dumps(bi_atestado_labels),
        "bi_atestado_data":    json.dumps(bi_atestado_data),
    }

    return render(request, "superusuario/painel_super.html", contexto)


@login_required
def painel_professor(request):
    """Dashboard principal para Professores."""
    professor = getattr(request.user, 'professor', None)
    if not professor:
        return render(request, "core/sem_perfil.html")

    hoje = datetime.now()
    ano_atual = hoje.year
    
    # Filtro de Ano Letivo
    from apps.calendario.models.calendario import EventoCalendario
    anos_turmas = list(
        Turma.objects.filter(disciplinas__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
    )
    anos_cal = list(EventoCalendario.objects.dates('data', 'year').values_list('data__year', flat=True).distinct())
    anos_unidos = set(anos_turmas + anos_cal)
    if not anos_unidos:
        anos_unidos.add(ano_atual)
    anos_disponiveis = sorted(list(anos_unidos), reverse=True)
    
    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    # Disciplinas e Turmas vinculadas ao professor no ano selecionado
    from apps.academico.models.academico import Disciplina
    disciplinas = Disciplina.objects.filter(
        professor=professor, 
        turma__ano=ano_filtro
    ).select_related("turma")
    
    turmas_ids = disciplinas.values_list("turma_id", flat=True).distinct()
    
    # Calcular métricas via utilitário acumulador
    from apps.academico.utils.academico import _acumular_notas_professor
    total_possiveis, total_lancadas, total_alunos_unicos, _ = _acumular_notas_professor(disciplinas)

    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[hoje.month - 1].upper()

    contexto = {
        "professor":               professor,
        "nome_exibicao":           get_nome_exibicao(request.user),
        "foto_perfil_url":         get_foto_perfil(request.user),
        "agora":                   hoje,
        "mes_nome":                mes_nome,
        "calendario":              gerar_calendario(ano_atual, hoje.month, user=request.user),
        "ano_calendario":          ano_atual,
        "total_turmas":            turmas_ids.count(),
        "total_alunos":            total_alunos_unicos,
        "total_disciplinas":       disciplinas.count(),
        "total_notas_lancadas":    total_lancadas,
        "total_notas_possiveis":   total_possiveis,
        "anos_disponiveis":        anos_disponiveis,
        "ano_filtro":              ano_filtro,
        "comunicados": Comunicado.objects.filter(
            Q(publico_alvo__in=['GLOBAL', 'PROFESSORES']),
            Q(data_expiracao__gte=timezone.now().date()) | Q(data_expiracao__isnull=True)
        )[:5],
    }
    
    from apps.biblioteca.models.biblioteca import Emprestimo
    contexto["meus_emprestimos"] = Emprestimo.objects.filter(
        usuario_professor=professor
    ).exclude(status='DEVOLVIDO').select_related('livro').order_by('-data_emprestimo')
    
    contexto["livros_devolvidos"] = Emprestimo.objects.filter(
        usuario_professor=professor, 
        status='DEVOLVIDO'
    ).select_related('livro').order_by('-data_devolucao_real')[:10]

    return render(request, "professor/painel_professor.html", contexto)


@login_required
def painel_aluno(request):
    """Dashboard principal para Alunos."""
    aluno = getattr(request.user, 'aluno', None)
    
    # Se o usuário for Responsável, ele pode ver o dashboard de um dependente
    if not aluno and hasattr(request.user, 'responsavel'):
        aluno_id = request.GET.get('aluno_id')
        if aluno_id:
            aluno = request.user.responsavel.alunos.filter(id=aluno_id).first()

    if not aluno:
        return render(request, "core/sem_perfil.html")

    # Calcular intervalo da semana atual para marcar suspensões na grade
    hoje_date = timezone.now().date()
    start_week = hoje_date - timedelta(days=hoje_date.weekday())
    end_week = start_week + timedelta(days=4)
    
    grade = _get_grade_horario_turma(aluno.turma, data_inicio=start_week, data_fim=end_week)
    
    from apps.academico.models.academico import Disciplina, PlanejamentoAula, MaterialDidatico
    from apps.academico.models.desempenho import Nota, Frequencia
    from apps.academico.utils.academico import _calcular_situacao_nota
    
    from apps.academico.selectors.desempenho_selectors import DesempenhoSelector
    
    disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
    
    disciplinas_com_notas = []
    soma_medias = 0
    total_disciplinas_com_media = 0
    total_notas_possiveis = disciplinas.count() * 4
    total_notas_lancadas = 0

    # Otimização: Buscar todos os planejamentos e materiais de uma vez para evitar N+1
    todos_planejamentos = PlanejamentoAula.objects.filter(turma=aluno.turma).order_by('-data_aula')
    todos_materiais = MaterialDidatico.objects.filter(disciplina__turma=aluno.turma).select_related('livro')

    for disciplina in disciplinas:
        # Pega a nota pré-carregada (to_attr do selector)
        nota = disciplina.nota_aluno_prefetched[0] if disciplina.nota_aluno_prefetched else None
        
        if nota:
            for n in [nota.nota1, nota.nota2, nota.nota3, nota.nota4]:
                if n is not None:
                    total_notas_lancadas += 1
            if nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1
        
        # Pega as frequências pré-carregadas
        frequencias_aluno = disciplina.frequencias_aluno_prefetched
        total_aulas = len(frequencias_aluno)
        faltas = len([f for f in frequencias_aluno if not f.presente])
        percentual_faltas = (faltas / total_aulas * 100) if total_aulas > 0 else 0
        
        # Filtra na memória (muito mais rápido que Query no DB)
        planejamentos = [p for p in todos_planejamentos if p.disciplina_id == disciplina.id][:10]
        materiais = [m for m in todos_materiais if m.disciplina_id == disciplina.id][:3]

        disciplinas_com_notas.append({
            'disciplina': disciplina,
            'nota': nota,
            'total_aulas': total_aulas,
            'faltas': faltas,
            'percentual_faltas': int(percentual_faltas),
            'planejamentos': planejamentos,
            'materiais_recentes': materiais
        })
        
    media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0
    
    freq_total = Frequencia.objects.filter(aluno=aluno)
    total_aulas_gerais = freq_total.count()
    faltas_gerais = freq_total.filter(presente=False).count()
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
    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[agora.month - 1].title()

    from apps.biblioteca.models.biblioteca import Emprestimo
    emprestimos = Emprestimo.objects.filter(usuario_aluno=aluno).exclude(status='DEVOLVIDO').select_related('livro').order_by('-data_emprestimo')
    devolvidos  = Emprestimo.objects.filter(usuario_aluno=aluno, status='DEVOLVIDO').select_related('livro').order_by('-data_devolucao_real')[:10]

    contexto = {
        "aluno":                 aluno,
        "nome_exibicao":         get_nome_exibicao(request.user),
        "foto_perfil_url":       get_foto_perfil(request.user),
        "agora":                 agora,
        "mes_nome":              mes_nome,
        "calendario":            gerar_calendario(ano_atual, agora.month, user=request.user),
        "ano_calendario":        ano_atual,
        "grade_horario":         grade,
        "disciplinas_com_notas": disciplinas_com_notas,
        "media_geral":           media_geral,
        "situacao_geral":        situacao_geral,
        "situacao_classe":       situacao_classe,
        "total_notas_lancadas":  total_notas_lancadas,
        "total_notas_possiveis": total_notas_possiveis,
        "notificacoes_recentes": Notificacao.objects.filter(usuario=request.user).order_by("-criado_em")[:8],
        "notificacoes_nao_lidas": Notificacao.objects.filter(usuario=request.user, lida=False).count(),
        "comunicados": Comunicado.objects.filter(
            Q(publico_alvo__in=['GLOBAL', 'ALUNOS']),
            Q(data_expiracao__gte=timezone.now().date()) | Q(data_expiracao__isnull=True)
        )[:5],
        "meus_emprestimos": emprestimos,
        "livros_devolvidos": devolvidos,
    }

    return render(request, "aluno/painel_aluno.html", contexto)


@login_required
def painel_responsavel(request):
    """Dashboard para pais/responsáveis acompanharem seus dependentes."""
    responsavel = getattr(request.user, 'responsavel', None)
    if not responsavel:
        return render(request, "core/sem_perfil.html")

    dependentes = responsavel.alunos.all().select_related('turma')
    
    # Se tiver apenas um dependente, já podemos facilitar a visualização
    # Mas o layout deve suportar múltiplos (ex: dois irmãos)
    
    dependentes_resumo = []
    from apps.academico.selectors.desempenho_selectors import DesempenhoSelector
    from apps.academico.utils.academico import _calcular_situacao_nota

    for aluno in dependentes:
        disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
        
        soma_medias = 0
        total_disciplinas_com_media = 0
        
        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            if nota and nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1
        
        media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0
        
        from apps.academico.models.desempenho import Frequencia
        freq_total = Frequencia.objects.filter(aluno=aluno)
        total_aulas_gerais = freq_total.count()
        faltas_gerais = freq_total.filter(presente=False).count()
        percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)

        sit_dict = _calcular_situacao_nota(media_geral, percentual_frequencia_geral)
        
        dependentes_resumo.append({
            'aluno': aluno,
            'media_geral': media_geral,
            'frequencia': percentual_frequencia_geral,
            'situacao': sit_dict,
            'total_disciplinas': disciplinas.count()
        })

    contexto = {
        "responsavel": responsavel,
        "dependentes": dependentes_resumo,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    }

    return render(request, "responsavel/painel_responsavel.html", contexto)


@login_required
def painel_usuarios(request):
    """Redirecionador para os painéis específicos."""
    from ..utils.perfis import redirect_user
    return render(request, "core/usuarios.html", {
        "nome_exibicao":     get_nome_exibicao(request.user),
        "foto_perfil_url":   get_foto_perfil(request.user),
    })


@login_required
def dashboard_redirect(request):
    """URL central 'dashboard' que redireciona para o painel correto do usuário."""
    from ..utils.perfis import redirect_user
    from django.shortcuts import redirect
    target = redirect_user(request.user)
    return redirect(target)

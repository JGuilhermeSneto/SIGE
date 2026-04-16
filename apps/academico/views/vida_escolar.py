"""
Views de lançamento pedagógico: notas bimestrais e frequência (chamada).

O que é: opera sobre ``models.desempenho`` e ``Disciplina``; restrito a
professores (ou outros papéis definidos nos decorators).
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import date
from django.db.models import Count, Q
from django.urls import reverse

from ..models.desempenho import Nota, Frequencia
from ..models.academico import Disciplina
from apps.saude.models.ficha_medica import AtestadoMedico
from apps.usuarios.models.perfis import Aluno
from apps.usuarios.utils.perfis import (
    get_nome_exibicao, get_foto_perfil, is_super_ou_gestor,
    redirect_user
)
from ..utils.academico import _contar_notas_lancadas
from ..services.notificacao_servico import NotificacaoServico

@login_required
def lancar_nota(request, disciplina_id):
    """Lançamento de notas bimestrais."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    eh_professor = hasattr(request.user, "professor") and disciplina.professor == request.user.professor
    if not (is_super_ou_gestor(request.user) or eh_professor):
        messages.error(request, "Acesso negado.")
        return redirect("dashboard")

    alunos = Aluno.objects.filter(turma_id=disciplina.turma_id).select_related("user").order_by("nome_completo")

    if request.method == "POST":
        for aluno in alunos:
            nota_obj, _ = Nota.objects.get_or_create(aluno_id=aluno.pk, disciplina_id=disciplina.id)
            for i in range(1, 5):
                valor = request.POST.get(f"nota{i}_{aluno.pk}", "").strip()
                if valor == "": setattr(nota_obj, f"nota{i}", None)
                else:
                    try:
                        v = float(valor.replace(",", "."))
                        if 0 <= v <= 10: setattr(nota_obj, f"nota{i}", v)
                    except ValueError: messages.error(request, f"Erro na nota {i} de {aluno.nome_completo}")
            nota_obj.save()
            media_txt = f"{nota_obj.media:.2f}" if nota_obj.media is not None else "N/A"
            NotificacaoServico.criar(
                aluno=aluno,
                tipo="NOTA",
                titulo="Notas bimestrais atualizadas",
                mensagem=f"{disciplina.nome}: suas notas foram atualizadas (média atual {media_txt}).",
                url_destino="/academico/meu-painel/atividades/",
            )
        messages.success(request, "Notas salvas!")
        return redirect("lancar_nota", disciplina_id=disciplina.id)

    notas_dict = {n.aluno_id: n for n in Nota.objects.filter(disciplina_id=disciplina.id)}
    return render(request, "professor/lancar_nota.html", {
        "disciplina": disciplina, "alunos": alunos, "notas_dict": notas_dict,
        "is_gestor_ou_super": is_super_ou_gestor(request.user),
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def lancar_chamada(request, disciplina_id):
    """Realiza a chamada diária."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    eh_professor = hasattr(request.user, "professor") and disciplina.professor == request.user.professor
    if not (is_super_ou_gestor(request.user) or eh_professor):
        messages.error(request, "Acesso negado.")
        return redirect("disciplinas_professor")

    data_str = request.GET.get("data") or request.POST.get("data")
    try: data_sel = date.fromisoformat(data_str) if data_str else timezone.now().date()
    except: data_sel = timezone.now().date()

    alunos = disciplina.turma.alunos.all().order_by("nome_completo")
    freq_obs = {f.aluno_id: f for f in Frequencia.objects.filter(disciplina=disciplina, data=data_sel)}
    
    # IDs de usuários com atestado aprovado para este dia
    ids_usuarios_de_atestado = AtestadoMedico.objects.filter(
        status='APROVADO',
        data_inicio__lte=data_sel,
        data_fim__gte=data_sel
    ).values_list('usuario_id', flat=True)

    if request.method == "POST":
        presentes = request.POST.getlist("presentes")
        for aluno in alunos:
            pres = str(aluno.id) in presentes
            obs = request.POST.get(f"observacao_{aluno.id}", "").strip() if not pres else ""
            Frequencia.objects.update_or_create(
                aluno=aluno, disciplina=disciplina, data=data_sel,
                defaults={"presente": pres, "observacao": obs}
            )
            status = "Presença registrada" if pres else "Falta registrada"
            detalhe = "Você foi marcado como presente." if pres else "Você foi marcado com falta."
            NotificacaoServico.criar(
                aluno=aluno,
                tipo="CHAMADA",
                titulo=status,
                mensagem=f"{disciplina.nome} ({data_sel.strftime('%d/%m/%Y')}): {detalhe}",
                url_destino="/academico/frequencia/aluno/",
            )
        messages.success(request, "Chamada salva!")
        return redirect(f"{reverse('lancar_chamada', args=[disciplina.id])}?data={data_sel}")

    return render(request, "frequencia/lancar_chamada.html", {
        "disciplina": disciplina, "alunos": alunos, "data_selecionada": data_sel.isoformat(), "data_formatada": data_sel.strftime("%d/%m/%Y"),
        "frequencias_existentes": freq_obs, 
        "ids_usuarios_de_atestado": list(ids_usuarios_de_atestado),
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def historico_frequencia(request, disciplina_id):
    """Resumo de chamadas."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if not (is_super_ou_gestor(request.user) or (hasattr(request.user, "professor") and disciplina.professor == request.user.professor)):
        return redirect("disciplinas_professor")

    resumo = Frequencia.objects.filter(disciplina=disciplina).values("data").annotate(
        total=Count("id"), presencas=Count("id", filter=Q(presente=True)), faltas=Count("id", filter=Q(presente=False))
    ).order_by("-data")

    return render(request, "frequencia/historico_frequencia.html", {
        "disciplina": disciplina, "resumo_por_data": resumo, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def frequencia_aluno(request):
    """Histórico do aluno."""
    if not hasattr(request.user, "aluno"): return redirect(redirect_user(request.user))
    aluno = request.user.aluno
    freqs = Frequencia.objects.filter(aluno=aluno).values("disciplina__nome").annotate(
        total_aulas=Count("id"),
        presencas=Count("id", filter=Q(presente=True)),
        faltas=Count("id", filter=Q(presente=False))
    ).order_by("disciplina__nome")

    return render(request, "frequencia/frequencia_aluno.html", {
        "aluno": aluno, "frequencias": freqs, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

def _calcular_situacao_aluno(disciplinas_com_notas, total_lancadas, total_possiveis):
    """Define situação geral do aluno."""
    if total_possiveis == 0: return "Sem Dados", "info"
    medias = [d["nota"].media for d in disciplinas_com_notas if d["nota"] and d["nota"].media is not None]
    if not medias: return "Cursando", "warning"
    mf = sum(medias) / len(medias)
    if mf >= 7: return "Aprovado", "success"
    if mf >= 5: return "Recuperação", "warning"
    return "Reprovado", "danger"

def _coletar_notas_aluno(aluno, disciplinas):
    """Agrega todas as notas e freq do aluno."""
    notas = {n.disciplina_id: n for n in Nota.objects.filter(aluno=aluno)}
    f_agreg = Frequencia.objects.filter(aluno=aluno).values("disciplina_id").annotate(
        total=Count("id"), presencas=Count("id", filter=Q(presente=True))
    )
    f_dict = {f["disciplina_id"]: f for f in f_agreg}
    detalhes = []
    s_med, t_med, t_lanc = 0, 0, 0
    for d in disciplinas:
        nota = notas.get(d.id)
        t_lanc += _contar_notas_lancadas(d, aluno.turma)
        f = f_dict.get(d.id, {"total": 0, "presencas": 0})
        detalhes.append({
            "disciplina": d, "nota": nota, "total_aulas": f["total"], "presencas": f["presencas"], "faltas": f["total"] - f["presencas"],
            "percentual_faltas": round(((f["total"] - f["presencas"]) / f["total"] * 100), 1) if f["total"] > 0 else 0
        })
        if nota and nota.media is not None:
            s_med += float(nota.media)
            t_med += 1
    return detalhes, (s_med / t_med if t_med > 0 else None), t_lanc

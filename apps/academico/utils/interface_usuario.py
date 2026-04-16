"""
Montagem de dados de calendário para dashboards (grade visual mensal).

O que é: lê ``EventoCalendario`` e monta estrutura consumida pelos templates
de painel e pela view principal do app ``calendario``.
"""

import calendar
from django.utils.timezone import now

def gerar_calendario(ano=None, mes=None, user=None):
    """Gera dados para o mini-calendário, agora identificando suspensões por usuário."""
    from apps.calendario.models.calendario import EventoCalendario
    from apps.academico.models.academico import PlanejamentoAula
    from django.db.models import Q
    
    hoje = now().date()
    ano = ano or hoje.year
    mes = mes or hoje.month
    
    cal = calendar.Calendar(firstweekday=6)
    dias_mes = cal.monthdatescalendar(ano, mes)

    data_inicio = dias_mes[0][0]
    data_fim = dias_mes[-1][-1]
    
    # Eventos globais
    eventos = EventoCalendario.objects.filter(data__range=(data_inicio, data_fim))
    eventos_dict = {ev.data: ev for ev in eventos}

    # Suspensões específicas do usuário
    suspensoes_usuario = set()
    if user:
        filtro_user = Q()
        if hasattr(user, 'professor'):
            filtro_user = Q(professor=user.professor)
        elif hasattr(user, 'aluno'):
            filtro_user = Q(turma=user.aluno.turma)
        
        if filtro_user:
            dias_suspensos = PlanejamentoAula.objects.filter(
                filtro_user,
                data_aula__range=(data_inicio, data_fim),
                status='SUSPENSA'
            ).values_list('data_aula', flat=True).distinct()
            suspensoes_usuario = set(dias_suspensos)

    calendario_flat = []
    for semana in dias_mes:
        for d in semana:
            is_hoje = (d == hoje)
            is_mes_atual = (d.month == mes)
            
            evento = eventos_dict.get(d)
            tipo = evento.tipo if evento else ('FIM_SEMANA' if d.weekday() in [5, 6] else 'DI_LETIVO')
            descricao = evento.descricao if evento else ''
            
            # Aula suspensa se houver evento global OU se o usuário específico tiver aula suspensa nesse dia
            aula_suspensa_global = bool(getattr(evento, "aula_suspensa", False))
            aula_suspensa_pessoal = d in suspensoes_usuario
            aula_suspensa = aula_suspensa_global or aula_suspensa_pessoal
            
            tem_evento = bool(descricao and descricao.strip())
            
            if tem_evento and aula_suspensa:
                status_tooltip = "Evento + Aula suspensa"
            elif tem_evento:
                status_tooltip = "Evento"
            elif aula_suspensa:
                status_tooltip = "Sua aula está suspensa" if aula_suspensa_pessoal else "Aula suspensa"
            else:
                status_tooltip = ""
            
            calendario_flat.append({
                "numero": d.day,
                "data": d.strftime('%Y-%m-%d'),
                "vazio": not is_mes_atual,
                "hoje": is_hoje,
                "tipo": tipo,
                "descricao": descricao,
                "aula_suspensa": aula_suspensa,
                "tem_evento": tem_evento,
                "status_tooltip": status_tooltip,
            })
    return calendario_flat

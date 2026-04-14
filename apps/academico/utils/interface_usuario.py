"""
Montagem de dados de calendário para dashboards (grade visual mensal).

O que é: lê ``EventoCalendario`` e monta estrutura consumida pelos templates
de painel e pela view principal do app ``calendario``.
"""

import calendar
from django.utils.timezone import now

def gerar_calendario(ano=None, mes=None):
    """Gera dados para o mini-calendário do dashboard com base no banco de dados."""
    from apps.calendario.models.calendario import EventoCalendario
    
    hoje = now().date()
    ano = ano or hoje.year
    mes = mes or hoje.month
    
    cal = calendar.Calendar(firstweekday=6)
    dias_mes = cal.monthdatescalendar(ano, mes)

    # Buscar eventos do mês e das pontas (dias preenchidos de outros meses) para evitar N+1
    data_inicio = dias_mes[0][0]
    data_fim = dias_mes[-1][-1]
    eventos = EventoCalendario.objects.filter(data__range=(data_inicio, data_fim))
    eventos_dict = {ev.data: ev for ev in eventos}

    calendario_flat = []
    for semana in dias_mes:
        for d in semana:
            is_hoje = (d == hoje)
            is_mes_atual = (d.month == mes)
            
            evento = eventos_dict.get(d)
            tipo = evento.tipo if evento else ('FIM_SEMANA' if d.weekday() in [5, 6] else 'DI_LETIVO')
            descricao = evento.descricao if evento else ''
            
            calendario_flat.append({
                "numero": d.day,
                "data": d.strftime('%Y-%m-%d'),
                "vazio": not is_mes_atual,
                "hoje": is_hoje,
                "tipo": tipo,
                "descricao": descricao
            })
    return calendario_flat

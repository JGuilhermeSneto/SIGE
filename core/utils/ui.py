import calendar
from django.utils.timezone import now

def gerar_calendario(ano=None, mes=None):
    """Gera dados para o mini-calendário do dashboard com base no banco de dados."""
    from ..models import EventoCalendario
    
    hoje = now().date()
    ano = ano or hoje.year
    mes = mes or hoje.month
    
    cal = calendar.Calendar(firstweekday=6)
    dias_mes = cal.monthdatescalendar(ano, mes)

    # Buscar eventos do mês de uma vez para evitar N+1
    eventos = EventoCalendario.objects.filter(data__year=ano, data__month=mes)
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

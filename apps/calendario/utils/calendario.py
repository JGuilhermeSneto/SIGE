"""
Funções puras de calendário: Páscoa, geração de grade anual, regras de dia letivo.

O que é: algoritmos sem acesso a ``request``; usados pelas views ao criar/atualizar
``EventoCalendario`` em lote.
"""

from datetime import date, timedelta


def get_pascoa(ano):
    """Calcula a data do domingo de Páscoa usando o algoritmo de Meeus/Jones/Butcher."""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) // 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)

def get_feriados_nacionais(ano):
    """Retorna um dicionário {data: 'nome'} com feriados nacionais brasileiros."""
    pascoa = get_pascoa(ano)
    
    feriados = {
        # Fixos
        date(ano, 1, 1): "Confraternização Universal",
        date(ano, 4, 21): "Tiradentes",
        date(ano, 5, 1): "Dia do Trabalho",
        date(ano, 9, 7): "Independência do Brasil",
        date(ano, 10, 12): "Nossa Senhora Aparecida",
        date(ano, 11, 2): "Finados",
        date(ano, 11, 15): "Proclamação da República",
        date(ano, 11, 20): "Consciência Negra",
        date(ano, 12, 25): "Natal",
        
        # Móveis
        pascoa - timedelta(days=48): "Segunda-feira de Carnaval",
        pascoa - timedelta(days=47): "Terça-feira de Carnaval",
        pascoa - timedelta(days=2): "Sexta-feira Santa",
        pascoa + timedelta(days=60): "Corpus Christi",
    }
    return feriados

def is_fim_semana(data):
    """Retorna True se for Sábado (5) ou Domingo (6)."""
    return data.weekday() in [5, 6]

def gerar_base_calendario(ano):
    """Calcula a classificação base para todos os dias de um ano."""
    feriados = get_feriados_nacionais(ano)
    dias_base = {}
    
    data_ini = date(ano, 1, 1)
    data_fim = date(ano, 12, 31)
    
    delta = timedelta(days=1)
    atual = data_ini
    
    while atual <= data_fim:
        tipo = 'DI_LETIVO'
        descricao = ""
        aula_suspensa = False
        
        # Prioridade 1: Feriado
        if atual in feriados:
            tipo = 'FERIADO'
            descricao = feriados[atual]
            aula_suspensa = True
        
        # Prioridade 2: Final de Semana (se não for feriado)
        elif is_fim_semana(atual):
            tipo = 'FIM_SEMANA'
            descricao = "Final de Semana"
            aula_suspensa = True if atual.weekday() == 6 else False # Domingo sempre suspenso, sábado opcional (definimos depois)

        dias_base[atual] = {
            'tipo': tipo,
            'descricao': descricao,
            'aula_suspensa': aula_suspensa
        }
        atual += delta
        
    return dias_base

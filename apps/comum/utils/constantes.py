"""
Constantes de domínio compartilhadas (horários por turno).

O que é: dicionário ``HORARIOS`` usado na montagem de grades e telas que
exibem blocos de aula por manhã/tarde/noite.
"""

# =====================================================================
# Grade horária — faixas exibidas na UI
# =====================================================================

HORARIOS = {
    "manha": [
        "07:00 às 07:45",
        "07:45 às 08:30",
        "08:50 às 09:35",
        "09:35 às 10:20",
        "10:30 às 11:15",
        "11:15 às 12:00",
    ],
    "tarde": [
        "13:00 às 13:45",
        "13:45 às 14:30",
        "14:50 às 15:35",
        "15:35 às 16:20",
        "16:30 às 17:15",
        "17:15 às 18:00",
    ],
    "noite": [
        "19:00 às 19:45",
        "19:45 às 20:30",
        "20:40 às 21:25",
        "21:25 às 22:00",
    ],
}

DIAS_SEMANA = ["segunda", "terca", "quarta", "quinta", "sexta"]
NOMES_DIAS  = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

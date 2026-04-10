def _get_anos_filtro(anos_disponiveis, ano_selecionado, ano_atual):
    """Processa a seleção de ano letivo para filtros."""
    try:
        ano_filtro = int(ano_selecionado) if ano_selecionado else ano_atual
    except (ValueError, TypeError):
        ano_filtro = ano_atual

    lista_anos = list(anos_disponiveis)
    if ano_atual not in lista_anos:
        lista_anos.append(ano_atual)
    if ano_filtro not in lista_anos:
        lista_anos.append(ano_filtro)

    lista_anos.sort(reverse=True)
    return ano_filtro, lista_anos


def _get_ano_filtro_professor(request, anos_disponiveis, ano_atual):
    """Gerencia filtro de ano na sessão."""
    ano_param = request.GET.get("ano")
    if ano_param:
        try:
            ano_filtro = int(ano_param)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis = sorted(list(set(anos_disponiveis + [ano_filtro])), reverse=True)
    return ano_filtro, anos_disponiveis

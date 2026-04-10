from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime
import json

from ..models import EventoCalendario
from ..utils.calendario import gerar_base_calendario, get_pascoa
from ..utils import is_super_ou_gestor

@login_required
def visualizar_calendario(request):
    """Exibe o calendário acadêmico para todos os usuários."""
    from ..utils.ui import gerar_calendario
    
    hoje = timezone.now()
    ano = int(request.GET.get('ano', hoje.year))
    mes = int(request.GET.get('mes', hoje.month))
    
    # Lógica de correção de mês (Janeiro - 1 = Dezembro Ano Anterior)
    if mes > 12:
        mes = 1
        ano += 1
    elif mes < 1:
        mes = 12
        ano -= 1
        
    dias_dados = gerar_calendario(ano, mes)
    
    context = {
        'ano_filtro': ano,
        'mes_filtro': mes,
        'dias_calendario': dias_dados,
        'pode_gerenciar': is_super_ou_gestor(request.user),
        'anos_disponiveis': range(hoje.year - 2, hoje.year + 3)
    }
    return render(request, 'core/calendario.html', context)

@login_required
@user_passes_test(is_super_ou_gestor)
def ajustar_dia_calendario(request):
    """AJAX: Ajusta um dia específico do calendário."""
    if request.method == 'POST':
        try:
            data_str = request.POST.get('data')
            tipo = request.POST.get('tipo')
            descricao = request.POST.get('descricao', '')
            aula_suspensa = request.POST.get('aula_suspensa') == 'true'
            
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
            
            evento, created = EventoCalendario.objects.update_or_create(
                data=data_obj,
                defaults={
                    'tipo': tipo,
                    'descricao': descricao,
                    'aula_suspensa': aula_suspensa
                }
            )
            
            return JsonResponse({'success': True, 'msg': 'Dia atualizado com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})
            
    return JsonResponse({'success': False, 'msg': 'Método inválido.'})

@login_required
@user_passes_test(is_super_ou_gestor)
def gerar_base_ano(request):
    """Gera a base de feriados e fins de semana para um ano específico."""
    if request.method == 'POST':
        ano = int(request.POST.get('ano', timezone.now().year))
        
        # Opcional: Limpar ano antes de gerar? 
        # Decidimos apenas sobrepor para não perder descrições manuais se o gestor apenas quiser 'refresh'
        #Ajustar o calendario para exibir nos usuarios
        # Dias não estão sendo salvos para os usuários
        
        dados_base = gerar_base_calendario(ano)
        
        for data_obj, info in dados_base.items():
            # Não sobrepõe se já existir algo com descrição manual rica? 
            # Como é uma ação de 'Gerar Base', vamos atualizar os padrões.
            EventoCalendario.objects.update_or_create(
                data=data_obj,
                defaults={
                    'tipo': info['tipo'],
                    'descricao': info['descricao'],
                    'aula_suspensa': info['aula_suspensa']
                }
            )
            
        messages.success(request, f"Base do calendário de {ano} gerada com sucesso!")
        return redirect('visualizar_calendario')
        
    return JsonResponse({'success': False, 'msg': 'POST necessário.'})

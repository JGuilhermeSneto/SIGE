from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models.biblioteca import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil, get_user_profile
from apps.usuarios.models.perfis import Aluno, Professor

@login_required
def acervo_biblioteca(request):
    """Consulta de livros disponível para Alunos, Professores e Gestores."""
    query = request.GET.get('q', '').strip()
    livros = Livro.objects.all().order_by('titulo')
    
    if query:
        livros = livros.filter(titulo__icontains=query) | livros.filter(autor__icontains=query)
        
    return render(request, 'biblioteca/acervo.html', {
        'livros': livros,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
        'is_gestor': is_super_ou_gestor(request.user),
    })

@login_required
def detalhe_livro(request, pk):
    """Exibe os detalhes de um livro específico do acervo."""
    livro = get_object_or_404(Livro, pk=pk)
    
    return render(request, 'biblioteca/detalhe_livro.html', {
        'livro': livro,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
        'is_gestor': is_super_ou_gestor(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def gerenciar_emprestimos(request):
    """Painel de controle de empréstimos e reservas (Somente Gestores)."""
    # Empréstimos que ainda não foram devolvidos
    emprestimos = Emprestimo.objects.filter(data_devolucao_real__isnull=True).order_by('status', 'data_devolucao_prevista')
    
    return render(request, 'biblioteca/gerenciar_emprestimos.html', {
        'emprestimos': emprestimos,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
        'hoje': timezone.now().date(),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def novo_emprestimo(request):
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            if emprestimo.livro.exemplares_disponiveis > 0:
                emprestimo.save()
                messages.success(request, f"Empréstimo de '{emprestimo.livro.titulo}' registrado!")
                return redirect('gerenciar_emprestimos')
            else:
                messages.error(request, "Este livro não possui exemplares disponíveis no momento.")
    else:
        # Pre-seleciona data de devolução para 14 dias
        data_prevista = timezone.now().date() + timedelta(days=14)
        form = EmprestimoForm(initial={'data_devolucao_prevista': data_prevista})
        
    return render(request, 'biblioteca/form_emprestimo.html', {
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def registrar_devolucao(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    emprestimo.data_devolucao_real = timezone.now().date()
    emprestimo.status = 'DEVOLVIDO'
    emprestimo.save()
    messages.success(request, f"Livro '{emprestimo.livro.titulo}' devolvido com sucesso!")
    return redirect('gerenciar_emprestimos')

@login_required
def reservar_livro(request, pk):
    """Permite que Alunos e Professores reservem um exemplar."""
    livro = get_object_or_404(Livro, pk=pk)
    perfil = get_user_profile(request.user)
    
    if not perfil or not (isinstance(perfil, Aluno) or isinstance(perfil, Professor)):
        messages.error(request, "Apenas alunos e professores podem reservar livros.")
        return redirect('acervo_biblioteca')

    # Valida estoque
    if livro.exemplares_disponiveis <= 0:
        messages.error(request, "Não há exemplares disponíveis para reserva.")
        return redirect('acervo_biblioteca')

    # Limite de 2 reservas/empréstimos ativos para alunos
    if isinstance(perfil, Aluno):
        ativos = Emprestimo.objects.filter(usuario_aluno=perfil, data_devolucao_real__isnull=True).count()
        if ativos >= 2:
            messages.warning(request, "Você já possui 2 reservas ou empréstimos ativos. Devolva um livro para liberar espaço!")
            return redirect('acervo_biblioteca')

    # Cria a reserva
    data_prevista = timezone.now().date() + timedelta(days=2) # 48h para retirar
    reserva = Emprestimo(
        livro=livro,
        status='RESERVA',
        data_devolucao_prevista=data_prevista
    )
    if isinstance(perfil, Aluno): reserva.usuario_aluno = perfil
    else: reserva.usuario_professor = perfil
    
    reserva.save()
    messages.success(request, f"Reserva de '{livro.titulo}' realizada! Você tem 48h para retirar na biblioteca.")
    return redirect('acervo_biblioteca')

@login_required
@user_passes_test(is_super_ou_gestor)
def confirmar_retirada(request, pk):
    """Gestor confirma que o aluno retirou o livro reservado."""
    reserva = get_object_or_404(Emprestimo, pk=pk, status='RESERVA')
    reserva.status = 'ATIVO'
    reserva.data_devolucao_prevista = timezone.now().date() + timedelta(days=14) # Ajusta prazo para 14 dias a partir de hoje
    reserva.save()
    messages.success(request, f"Retirada confirmada! Novo prazo: {reserva.data_devolucao_prevista.strftime('%d/%m/%Y')}")
    return redirect('gerenciar_emprestimos')

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro adicionado ao acervo!")
            return redirect('acervo_biblioteca')
    else:
        form = LivroForm()
    return render(request, 'biblioteca/form_livro.html', {'form': form})

@login_required
def atualizar_status_leitura(request):
    """Endpoint AJAX: atualiza o status_leitura de um Emprestimo devolvido do próprio aluno."""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'erro': 'Método inválido.'}, status=405)

    import json
    try:
        payload = json.loads(request.body)
        emprestimo_id  = int(payload.get('emprestimo_id', 0))
        status_leitura = payload.get('status_leitura', '').strip()
    except (ValueError, KeyError):
        return JsonResponse({'ok': False, 'erro': 'Dados inválidos.'}, status=400)

    VALIDOS = {'NAO_INFORMADO', 'LENDO', 'FINALIZADO'}
    if status_leitura not in VALIDOS:
        return JsonResponse({'ok': False, 'erro': 'Status inválido.'}, status=400)

    from apps.usuarios.utils.perfis import get_user_profile
    perfil = get_user_profile(request.user)
    
    if isinstance(perfil, Aluno):
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id, usuario_aluno=perfil, status='DEVOLVIDO')
    elif isinstance(perfil, Professor):
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id, usuario_professor=perfil, status='DEVOLVIDO')
    else:
        return JsonResponse({'ok': False, 'erro': 'Apenas alunos e professores podem atualizar.'}, status=403)

    emprestimo.status_leitura = status_leitura
    emprestimo.save(update_fields=['status_leitura'])
    return JsonResponse({'ok': True})

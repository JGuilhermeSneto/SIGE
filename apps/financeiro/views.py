from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Fatura, Pagamento
from django.db.models import Sum, Count, Q
from django.utils.timezone import now

@login_required
def listar_faturas(request):
    usuario = request.user
    status_filter = request.GET.get('status', 'todas')
    
    # Base queryset
    if hasattr(usuario, 'aluno'):
        faturas = Fatura.objects.filter(aluno=usuario.aluno)
    elif hasattr(usuario, 'gestor') or usuario.is_superuser:
        faturas = Fatura.objects.all()
    else:
        faturas = Fatura.objects.none()

    # Calculate "Atrasadas" (Pendente e Vencida)
    hoje = now().date()
    
    # Filter handling
    if status_filter == 'pendentes':
        faturas = faturas.filter(status='PENDENTE', data_vencimento__gte=hoje)
    elif status_filter == 'pagas':
        faturas = faturas.filter(status='PAGO')
    elif status_filter == 'atrasadas':
        faturas = faturas.filter(status='PENDENTE', data_vencimento__lt=hoje)

    faturas = faturas.order_by('data_vencimento')

    # Status counts for dashboard tabs
    total_faturas = faturas.count() if status_filter != 'todas' else Fatura.objects.filter(id__in=faturas).count()
    
    # Let's get total counts regardless of current filter to show on tabs
    base_qs = Fatura.objects.filter(aluno=usuario.aluno) if hasattr(usuario, 'aluno') else Fatura.objects.all()
    
    qtd_todas = base_qs.count()
    qtd_pendentes = base_qs.filter(status='PENDENTE', data_vencimento__gte=hoje).count()
    qtd_pagas = base_qs.filter(status='PAGO').count()
    qtd_atrasadas = base_qs.filter(status='PENDENTE', data_vencimento__lt=hoje).count()

    context = {
        'faturas': faturas,
        'status_filter': status_filter,
        'qtd_todas': qtd_todas,
        'qtd_pendentes': qtd_pendentes,
        'qtd_pagas': qtd_pagas,
        'qtd_atrasadas': qtd_atrasadas,
        'hoje': hoje,
    }
    return render(request, 'financeiro/listar_faturas.html', context)

@login_required
def relatorio_financeiro(request):
    # Only for gestores or superusers
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Acesso negado. Apenas gestores podem visualizar o relatório financeiro.")

    hoje = now().date()
    faturas = Fatura.objects.all()

    # Aggregate Data
    total_arrecadado = faturas.filter(status='PAGO').aggregate(Sum('valor'))['valor__sum'] or 0
    total_pendente = faturas.filter(status='PENDENTE', data_vencimento__gte=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    total_atrasado = faturas.filter(status='PENDENTE', data_vencimento__lt=hoje).aggregate(Sum('valor'))['valor__sum'] or 0

    qtd_pagas = faturas.filter(status='PAGO').count()
    qtd_pendentes = faturas.filter(status='PENDENTE', data_vencimento__gte=hoje).count()
    qtd_atrasadas = faturas.filter(status='PENDENTE', data_vencimento__lt=hoje).count()

    context = {
        'total_arrecadado': total_arrecadado,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'qtd_pagas': qtd_pagas,
        'qtd_pendentes': qtd_pendentes,
        'qtd_atrasadas': qtd_atrasadas,
        'hoje': hoje,
    }
    return render(request, 'financeiro/relatorio_financeiro.html', context)

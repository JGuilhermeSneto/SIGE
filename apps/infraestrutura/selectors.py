from django.db.models import Sum, F, Count, Q
from .models.patrimonio import ItemPatrimonio, SaldoEstoque, Ambiente, ManutencaoBem
import json

class InfraSelector:
    """Centraliza as consultas e métricas do módulo de Infraestrutura."""

    @staticmethod
    def get_painel_data(query_text=None):
        """Retorna todos os dados formatados para o dashboard de infraestrutura."""
        
        patrimonios = ItemPatrimonio.objects.all().select_related('categoria', 'unidade', 'responsavel', 'ambiente')
        saldos_estoque = SaldoEstoque.objects.all().select_related('item', 'unidade').order_by('item__nome')
        
        if query_text:
            patrimonios = patrimonios.filter(
                Q(nome__icontains=query_text) | 
                Q(tombamento__icontains=query_text) |
                Q(marca__icontains=query_text) |
                Q(ambiente__nome__icontains=query_text)
            )
            saldos_estoque = saldos_estoque.filter(item__nome__icontains=query_text)

        # ── Métricas ──────────────────────────────────────────────────
        metricas = {
            'total_patrimonio': patrimonios.count(),
            'valor_investido': patrimonios.aggregate(total=Sum('valor_aquisicao'))['total'] or 0,
            'manutencoes_pendentes': ManutencaoBem.objects.filter(data_realizacao__isnull=True).count(),
            'total_ambientes': Ambiente.objects.count(),
            'itens_criticos': saldos_estoque.filter(quantidade__lte=F('item__estoque_minimo')).count(),
            'estado_precario': patrimonios.filter(estado_conservacao__in=['DANIFICADO', 'INSERVIVEL']).count(),
        }

        # ── Dados para Gráficos ──────────────────────────────────────
        # Gráfico: Estado de Conservação
        dist_estado = {
            'labels': ['Novo/Bom', 'Regular', 'Danificado/Inservível'],
            'data': [
                patrimonios.filter(estado_conservacao__in=['NOVO', 'BOM']).count(),
                patrimonios.filter(estado_conservacao='REGULAR').count(),
                metricas['estado_precario']
            ]
        }
        
        # Gráfico: Categorias
        categorias_qs = ItemPatrimonio.objects.values('categoria__nome').annotate(total=Count('id')).order_by('-total')[:5]
        dist_categorias = {
            'labels': [c['categoria__nome'] for c in categorias_qs],
            'data': [c['total'] for c in categorias_qs]
        }

        return {
            'patrimonios': patrimonios,
            'saldos_estoque': saldos_estoque,
            'metricas': metricas,
            'dist_estado_json': json.dumps(dist_estado),
            'dist_categorias_json': json.dumps(dist_categorias),
        }

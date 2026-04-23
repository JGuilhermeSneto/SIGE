from rest_framework import viewsets, permissions
from .models import Fatura, Pagamento
from .serializers import FaturaSerializer, PagamentoSerializer

class FaturaViewSet(viewsets.ModelViewSet):
    queryset = Fatura.objects.all().select_related('aluno__user').prefetch_related('pagamentos')
    serializer_class = FaturaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return self.queryset.filter(aluno=user.aluno)
        elif hasattr(user, 'professor'):
            return self.queryset.none() # Professor não vê financeiro por padrão
        return self.queryset # Gestores/Admin veem tudo

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = [permissions.IsAuthenticated]

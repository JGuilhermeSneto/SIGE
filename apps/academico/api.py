from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models.desempenho import Notificacao

class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['id', 'tipo', 'titulo', 'mensagem', 'url_destino', 'lida', 'criado_em']

class NotificacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para listar e gerenciar notificações do usuário autenticado.
    Acesso universal: Qualquer usuário autenticado vê suas próprias notificações.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user).order_by('-criado_em')

    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        notificacao = self.get_object()
        notificacao.lida = True
        notificacao.save()
        return Response({'status': 'notificação marcada como lida', 'lida': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def marcar_todas_lidas(self, request):
        Notificacao.objects.filter(usuario=self.request.user, lida=False).update(lida=True)
        return Response({'status': 'todas notificações marcadas como lidas'}, status=status.HTTP_200_OK)

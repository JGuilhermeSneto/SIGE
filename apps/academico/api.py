from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models.desempenho import NotificacaoAluno

class NotificacaoAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificacaoAluno
        fields = ['id', 'tipo', 'titulo', 'mensagem', 'url_destino', 'lida', 'criado_em']

class NotificacaoAlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para listar e gerenciar notificações do aluno autenticado.
    Acesso restrito: Apenas alunos podem visualizar suas próprias notificações.
    """
    serializer_class = NotificacaoAlunoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return NotificacaoAluno.objects.filter(aluno=user.aluno).order_by('-criado_em')
        return NotificacaoAluno.objects.none()

    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        notificacao = self.get_object()
        notificacao.lida = True
        notificacao.save()
        return Response({'status': 'notificação marcada como lida', 'lida': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def marcar_todas_lidas(self, request):
        user = self.request.user
        if hasattr(user, 'aluno'):
            NotificacaoAluno.objects.filter(aluno=user.aluno, lida=False).update(lida=True)
            return Response({'status': 'todas notificações marcadas como lidas'}, status=status.HTTP_200_OK)
        return Response({'status': 'erro'}, status=status.HTTP_400_BAD_REQUEST)

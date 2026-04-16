from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import Livro, Emprestimo

class LivroSerializer(serializers.ModelSerializer):
    exemplares_disponiveis = serializers.IntegerField(read_only=True)
    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'isbn', 'ano_publicacao', 'editora', 'capa', 'quantidade_total', 'exemplares_disponiveis']

class EmprestimoSerializer(serializers.ModelSerializer):
    livro_titulo = serializers.CharField(source='livro.titulo', read_only=True)
    class Meta:
        model = Emprestimo
        fields = ['id', 'livro', 'livro_titulo', 'data_emprestimo', 'data_devolucao_prevista', 'status']
        read_only_fields = ['data_emprestimo', 'status']

class BibliotecaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lista o acervo da biblioteca. Permite alunos realizarem reservas, respeitando o limite de 2 livros.
    """
    queryset = Livro.objects.all().order_by('titulo')
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def reservar(self, request, pk=None):
        livro = self.get_object()
        user = request.user
        
        if not hasattr(user, 'aluno'):
            return Response({"detail": "Apenas alunos podem fazer reservas via web."}, status=status.HTTP_403_FORBIDDEN)
            
        aluno = user.aluno
        
        # Regra 1: Verificar se há exemplares
        if livro.exemplares_disponiveis <= 0:
            return Response({"detail": "Não há exemplares físicos disponíveis para reserva."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Regra 2: Validar o limite de 2 livros simultâneos
        livros_ativos = Emprestimo.objects.filter(
            usuario_aluno=aluno,
            status__in=['ATIVO', 'RESERVA']
        ).count()
        
        if livros_ativos >= 2:
            return Response({"detail": "Você já atingiu o limite máximo de 2 livros (entre reservas e ativos)."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Regra 3: Evitar reserva dupla do mesmo livro
        reserva_dupla = Emprestimo.objects.filter(
            usuario_aluno=aluno,
            livro=livro,
            status__in=['ATIVO', 'RESERVA']
        ).exists()
        
        if reserva_dupla:
            return Response({"detail": "Você já possui uma reserva ou empréstimo deste livro."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Efetuar reserva (7 dias para retirar na biblioteca)
        emprestimo = Emprestimo.objects.create(
            livro=livro,
            usuario_aluno=aluno,
            status='RESERVA',
            data_devolucao_prevista=timezone.now().date() + timedelta(days=7)
        )
        
        return Response({"detail": "Reserva efetuada com sucesso!", "emprestimo_id": emprestimo.id}, status=status.HTTP_201_CREATED)

class MeusEmprestimosViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista os empréstimos do aluno logado."""
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Emprestimo.objects.filter(usuario_aluno=user.aluno).order_by('-data_emprestimo')
        return Emprestimo.objects.none()

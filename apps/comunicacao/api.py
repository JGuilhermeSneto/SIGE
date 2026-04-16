from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Comunicado
from django.db.models import Q
from django.utils import timezone

class ComunicadoSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source="autor.nome_completo", read_only=True, default="Administração")
    publico_alvo_display = serializers.CharField(source='get_publico_alvo_display', read_only=True)
    ativo = serializers.BooleanField(source='esta_ativo', read_only=True)

    class Meta:
        model = Comunicado
        fields = [
            'id', 'titulo', 'conteudo', 'data_publicacao', 'data_expiracao',
            'publico_alvo', 'publico_alvo_display', 'autor_nome', 'importancia', 'ativo'
        ]

class ComunicadoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Comunicados to be viewed by authenticated users.
    Returns global communications and specific ones depending on the user's role.
    """
    serializer_class = ComunicadoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        hoje = timezone.now().date()
        
        # Filtra por comunicados ativos
        qs = Comunicado.objects.filter(
            Q(data_expiracao__isnull=True) | Q(data_expiracao__gte=hoje)
        )

        filters = Q(publico_alvo='GLOBAL')
        
        if hasattr(user, 'aluno'):
            filters |= Q(publico_alvo='ALUNOS')
        elif hasattr(user, 'professor'):
            filters |= Q(publico_alvo='PROFESSORES')
        elif hasattr(user, 'gestor'):
            filters |= Q(publico_alvo='GESTORES')
        elif user.is_superuser:
            # Superusers view everything
            return qs

        return qs.filter(filters).order_by('-data_publicacao')

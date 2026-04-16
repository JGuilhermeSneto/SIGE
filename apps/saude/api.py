from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FichaMedica, RegistroVacina

class RegistroVacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVacina
        fields = ['id', 'nome_vacina', 'data_dose', 'lote']

class FichaMedicaSerializer(serializers.ModelSerializer):
    vacinas = RegistroVacinaSerializer(many=True, read_only=True)
    aluno_nome = serializers.CharField(source='aluno.nome_completo', read_only=True)

    class Meta:
        model = FichaMedica
        fields = [
            'id', 'aluno_nome', 'tipo_sanguineo', 'alergias', 'medicamentos_continuos',
            'condicoes_pcd', 'detalhes_pcd', 'contato_emergencia_nome', 
            'contato_emergencia_fone', 'observacoes_medicas', 'vacinas'
        ]

class SaudeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para visualizar as fichas médicas.
    Regra de Segurança: Aluno vê a própria ficha.
    (Em um cenário real, professores veriam as fichas das próprias turmas, este endpoint de API
    neste estágio focará em entregar pro PWA do Aluno logado).
    """
    serializer_class = FichaMedicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'aluno'):
            return FichaMedica.objects.filter(aluno=user.aluno)
        # Se for gestor pode ver todos
        elif user.is_superuser or hasattr(user, 'gestor'):
            return FichaMedica.objects.all()
        return FichaMedica.objects.none()

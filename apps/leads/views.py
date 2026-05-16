from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lead, FunnelStage, LeadInteraction
from .serializers import LeadSerializer, FunnelStageSerializer, LeadInteractionSerializer
from .services import LeadService

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    @action(detail=True, methods=['post'])
    def converter(self, request, pk=None):
        """Endpoint para converter lead em aluno."""
        turma_id = request.data.get("turma_id")
        if not turma_id:
            return Response({"error": "turma_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            aluno = LeadService.converter_lead_em_aluno(pk, turma_id)
            return Response({
                "message": "Lead convertido com sucesso!",
                "aluno_id": aluno.id,
                "matricula": aluno.matricula
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FunnelStageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FunnelStage.objects.all()
    serializer_class = FunnelStageSerializer

class LeadInteractionViewSet(viewsets.ModelViewSet):
    queryset = LeadInteraction.objects.all()
    serializer_class = LeadInteractionSerializer

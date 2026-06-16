from rest_framework import viewsets, permissions
from .models import RFIDTag
from .serializers import RFIDTagSerializer

class RFIDTagViewSet(viewsets.ModelViewSet):
    """API CRUD para tags RFID. Usuários autenticados podem listar, criar, atualizar e excluir tags."""
    queryset = RFIDTag.objects.select_related('user').all()
    serializer_class = RFIDTagSerializer
    permission_classes = [permissions.IsAuthenticated]

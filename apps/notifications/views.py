from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import DeviceTokenSerializer
from .models import DeviceToken
from drf_spectacular.utils import extend_schema

class RegisterDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Mobile'],
        request=DeviceTokenSerializer,
        responses={200: DeviceTokenSerializer, 201: DeviceTokenSerializer},
        description="Registra ou atualiza um token de dispositivo para envio de notificações push."
    )
    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            token = serializer.save()
            return Response(DeviceTokenSerializer(token).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnregisterDeviceTokenView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Mobile'],
        request=DeviceTokenSerializer,
        responses={204: None},
        description="Desativa ou remove um token de dispositivo."
    )
    def post(self, request):
        token_str = request.data.get('token')
        if not token_str:
            return Response({"error": "O campo 'token' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            device = DeviceToken.objects.get(user=request.user, token=token_str)
            device.is_active = False
            device.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DeviceToken.DoesNotExist:
            return Response({"error": "Token não encontrado."}, status=status.HTTP_404_NOT_FOUND)

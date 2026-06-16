# 📂 Código do módulo IoT – RFID

## models.py
```python
from django.db import models
from django.conf import settings

class RFIDTag(models.Model):
    """Armazena o UID do tag RFID associado a um usuário (matrícula)."""
    uid = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rfid_tags",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uid} - {self.user.username}"
```

## serializers.py
```python
from rest_framework import serializers
from .models import RFIDTag

class RFIDTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDTag
        fields = ["id", "uid", "user", "created_at"]
        read_only_fields = ["id", "created_at"]
```

## views.py
```python
from rest_framework import viewsets, permissions
from .models import RFIDTag
from .serializers import RFIDTagSerializer

class RFIDTagViewSet(viewsets.ModelViewSet):
    """API CRUD para tags RFID."""
    queryset = RFIDTag.objects.select_related("user").all()
    serializer_class = RFIDTagSerializer
    permission_classes = [permissions.IsAuthenticated]
```

## urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RFIDTagViewSet

router = DefaultRouter()
router.register(r"rfid", RFIDTagViewSet, basename="iot-rfid")

urlpatterns = [
    path("", include(router.urls)),
]
```

## mqtt_consumer.py (exemplo simples)
```python
import os, django, json
import paho.mqtt.client as mqtt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from .models import RFIDTag
from django.contrib.auth import get_user_model
User = get_user_model()

BROKER_HOST = "192.168.18.90"
BROKER_PORT = 1883
TOPIC = "sige/iot/rfid"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    uid = msg.payload.decode().strip()
    print(f"Received UID: {uid}")
    # Exemplo: associa a usuário com ID 194 – ajuste conforme necessidade
    user = User.objects.get(id=194)
    RFIDTag.objects.update_or_create(uid=uid, defaults={"user": user})
    print("Tag saved/updated")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_forever()
```

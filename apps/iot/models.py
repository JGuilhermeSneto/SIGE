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

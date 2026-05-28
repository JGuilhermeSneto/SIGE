from django.db import models
from django.conf import settings

class DeviceToken(models.Model):
    PLATFORM_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True, verbose_name="Device Token")
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, verbose_name="Plataforma")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Device Token"
        verbose_name_plural = "Device Tokens"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.platform} ({'Ativo' if self.is_active else 'Inativo'})"

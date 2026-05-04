from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model
from axes.models import AccessLog, AccessAttempt
from django_otp.plugins.otp_totp.models import TOTPDevice
from apps.seguranca.models import LogAuditoria, LogErro

User = get_user_model()

class SecurityDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "seguranca/dashboard.html"

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, 'perfil') and self.request.user.perfil == 'gestor'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Logs de Auditoria (Áreas Sensíveis)
        context["logs_auditoria"] = LogAuditoria.objects.all().select_related("usuario")[:50]
        
        # Logs de Erros do Sistema (EXCEÇÕES)
        context["logs_erros"] = LogErro.objects.all().select_related("usuario")[:30]
        
        # Logs Administrativos (Painel Admin)
        context["logs_admin"] = LogEntry.objects.all().select_related("user", "content_type")[:20]
        
        # Logins bem sucedidos
        context["logins_sucesso"] = AccessLog.objects.all().order_by("-attempt_time")[:20]
        
        # Tentativas falhas
        context["tentativas_falhas"] = AccessAttempt.objects.all().order_by("-attempt_time")[:20]
        
        # Estatísticas de 2FA (MFA)
        total_usuarios = User.objects.count()
        usuarios_2fa = TOTPDevice.objects.filter(confirmed=True).values('user').distinct().count()
        context["stats_2fa"] = {
            "total": total_usuarios,
            "ativos": usuarios_2fa,
            "porcentagem": round((usuarios_2fa / total_usuarios * 100), 1) if total_usuarios > 0 else 0
        }

        # Sessões Ativas
        context["sessoes_ativas"] = Session.objects.filter(expire_date__gte=timezone.now()).count()
        
        # Resumo de bloqueios
        context["total_auditoria"] = LogAuditoria.objects.count()
        context["total_erros"] = LogErro.objects.count()
        context["bloqueios_ativos"] = AccessAttempt.objects.count()
        
        return context

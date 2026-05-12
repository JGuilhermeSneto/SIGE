from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from axes.models import AccessLog, AccessAttempt
from django_otp.plugins.otp_totp.models import TOTPDevice
from apps.seguranca.models import (
    LogAuditoria,
    LogErro,
    BlacklistIP,
    BugReport,
    ConfiguracaoSeguranca,
)
from apps.seguranca.utils.access import (
    pode_executar_acoes_seguranca,
    pode_ver_dashboard_seguranca,
)

User = get_user_model()


class SecurityDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Dashboard Shield — renderizado dentro do layout da área de TI (`ti/base_ti.html`)."""

    template_name = "seguranca/dashboard.html"

    def test_func(self):
        return pode_ver_dashboard_seguranca(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["pode_executar_acoes_seguranca"] = pode_executar_acoes_seguranca(user)
        context["config_seguranca"] = ConfiguracaoSeguranca.get_solo()

        # Paginação para logs de auditoria
        logs_auditoria = LogAuditoria.objects.all().select_related("usuario").order_by('-data_evento')
        paginator_auditoria = Paginator(logs_auditoria, 25)  # 25 por página
        page_auditoria = self.request.GET.get('page_auditoria', 1)
        context["logs_auditoria"] = paginator_auditoria.get_page(page_auditoria)

        # Paginação para logs de erro
        logs_erros = LogErro.objects.all().select_related("usuario").order_by('-data_ocorrencia')
        paginator_erros = Paginator(logs_erros, 20)  # 20 por página
        page_erros = self.request.GET.get('page_erros', 1)
        context["logs_erros"] = paginator_erros.get_page(page_erros)

        # Paginação para reports de bugs
        reports_bugs = BugReport.objects.all().select_related("usuario").order_by('-data_criacao')
        paginator_bugs = Paginator(reports_bugs, 15)  # 15 por página
        page_bugs = self.request.GET.get('page_bugs', 1)
        context["reports_bugs"] = paginator_bugs.get_page(page_bugs)

        # Paginação para blacklist IPs
        blacklist_ips = BlacklistIP.objects.all().select_related("bloqueado_por").order_by('-data_bloqueio')
        paginator_ips = Paginator(blacklist_ips, 20)  # 20 por página
        page_ips = self.request.GET.get('page_ips', 1)
        context["blacklist_ips"] = paginator_ips.get_page(page_ips)

        context["logs_admin"] = LogEntry.objects.all().select_related(
            "user", "content_type"
        )[:20]

        context["logins_sucesso"] = AccessLog.objects.all().order_by("-attempt_time")[
            :20
        ]

        context["tentativas_falhas"] = AccessAttempt.objects.all().order_by(
            "-attempt_time"
        )[:20]

        total_usuarios = User.objects.count()
        usuarios_2fa = (
            TOTPDevice.objects.filter(confirmed=True).values("user").distinct().count()
        )
        context["stats_2fa"] = {
            "total": total_usuarios,
            "ativos": usuarios_2fa,
            "porcentagem": (
                round((usuarios_2fa / total_usuarios * 100), 1)
                if total_usuarios > 0
                else 0
            ),
        }

        context["sessoes_ativas"] = Session.objects.filter(
            expire_date__gte=timezone.now()
        ).count()

        context["total_auditoria"] = LogAuditoria.objects.count()
        context["total_erros"] = LogErro.objects.count()
        context["total_bugs"] = BugReport.objects.filter(status="NOVO").count()
        context["bloqueios_ativos"] = BlacklistIP.objects.count()

        return context

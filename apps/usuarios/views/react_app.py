"""
Shell do app React (Vite) dentro do layout HTML do SIGE (``core/base.html``).

Em desenvolvimento, o template injeta os scripts do servidor Vite; em produção,
substitua por arquivos estáticos gerados com ``npm run build``.
"""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def app_vite_shell(request):
    """Renderiza o ``base.html`` com ``<div id=\"root\">`` para o React."""
    return render(
        request,
        "core/app_vite.html",
        {
            "use_vite_dev": settings.DEBUG,
            "vite_dev_url": getattr(
                settings, "VITE_DEV_SERVER_URL", "http://127.0.0.1:5173"
            ),
        },
    )

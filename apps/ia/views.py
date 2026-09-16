from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def assistente_status(request):
    """
    Retorna o status de prontidão do assistente ELISE IA.
    """
    return JsonResponse({
        "status": "ready",
        "assistant": "ELISE IA",
        "version": "1.0.0",
        "usuario": request.user.username,
    })

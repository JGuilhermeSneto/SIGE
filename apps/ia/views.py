from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import SessaoAssistente, MensagemAssistente, PropostaDecisao
from .services import perguntar, montar_contexto, verificar_disponibilidade_llm


def assistente_status(request):
    """
    Endpoint simples legado/compatibilidade para checagem rápida de status.
    """
    disponibilidade = verificar_disponibilidade_llm()
    return JsonResponse({
        "status": "ready",
        "assistant": "ELISE IA",
        "version": "1.0.0",
        "usuario": request.user.username if request.user.is_authenticated else "anonimo",
        "llm": disponibilidade,
    })


class StatusIAView(APIView):
    """
    Retorna o status completo do assistente, host Ollama e modelo Llama 3.1.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        info_llm = verificar_disponibilidade_llm()
        sessoes_ativas = SessaoAssistente.objects.filter(usuario=request.user, ativo=True).count()
        propostas_pendentes = PropostaDecisao.objects.filter(status="PENDENTE").count()

        return Response({
            "status": "online" if info_llm.get("disponivel") else "offline",
            "assistant": "ELISE IA - Apoio à Decisão",
            "usuario": request.user.username,
            "llm": info_llm,
            "metricas": {
                "sessoes_ativas": sessoes_ativas,
                "propostas_pendentes": propostas_pendentes,
            },
            "aviso": "Protótipo experimental de IA em ambiente de validação."
        })


class AssistenteChatView(APIView):
    """
    Endpoint principal de diálogo com o assistente (conforme Código 4 do TCC).
    Recebe a pergunta, injeta o contexto determinístico, executa a inferência
    e registra a auditoria completa da interação.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pergunta = request.data.get("pergunta", "").strip()
        sessao_id = request.data.get("sessao_id")
        tipo_contexto = request.data.get("tipo", "GERAL")

        if not pergunta:
            return Response(
                {"erro": "Informe uma pergunta para o assistente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Recupera ou cria uma sessão para o usuário
        if sessao_id:
            sessao = get_object_or_404(SessaoAssistente, id=sessao_id, usuario=request.user)
        else:
            titulo_auto = (pergunta[:40] + "...") if len(pergunta) > 40 else pergunta
            sessao = SessaoAssistente.objects.create(
                usuario=request.user,
                titulo=titulo_auto
            )

        # 2. Monta o contexto determinístico (RAG estruturado)
        contexto = montar_contexto(usuario=request.user, tipo=tipo_contexto)

        # 3. Registra a mensagem do usuário
        MensagemAssistente.objects.create(
            sessao=sessao,
            papel="user",
            conteudo=pergunta,
            contexto_utilizado=contexto
        )

        # 4. Chama a camada de serviço da LLM (Llama 3.1 8B via Ollama)
        resultado = perguntar(pergunta=pergunta, contexto=contexto)

        # 5. Registra a resposta do assistente com latência para fins de auditoria
        MensagemAssistente.objects.create(
            sessao=sessao,
            papel="assistant",
            conteudo=resultado["resposta"],
            latencia_segundos=resultado.get("latencia_segundos")
        )

        return Response({
            "sucesso": resultado.get("sucesso", True),
            "sessao_id": sessao.id,
            "resposta": resultado["resposta"],
            "latencia_segundos": resultado.get("latencia_segundos"),
            "modelo": resultado.get("modelo"),
            "aviso": resultado.get("aviso", "Protótipo experimental: valide as sugestões."),
        })


class PropostaDecisaoAcaoView(APIView):
    """
    Human-in-the-Loop: permite ao gestor aprovar ou rejeitar formalmente
    uma proposta sugerida pelo DSS.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        proposta = get_object_or_404(PropostaDecisao, pk=pk)
        acao = request.data.get("acao", "").upper()
        observacao = request.data.get("observacao", "")

        if acao not in ["APROVAR", "REJEITAR"]:
            return Response(
                {"erro": "Ação inválida. Escolha 'APROVAR' ou 'REJEITAR'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        proposta.status = "APROVADA" if acao == "APROVAR" else "REJEITADA"
        proposta.decidido_por = request.user
        proposta.decidido_em = timezone.now()
        if observacao:
            proposta.observacao_gestor = observacao
        proposta.save()

        return Response({
            "mensagem": f"Proposta '{proposta.titulo}' {proposta.get_status_display().lower()} com sucesso.",
            "status": proposta.status,
            "decidido_em": proposta.decidido_em,
            "decidido_por": request.user.username,
        })

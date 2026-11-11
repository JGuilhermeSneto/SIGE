from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import SessaoAssistente, MensagemAssistente, PropostaDecisao
from .services import (
    perguntar,
    montar_contexto,
    verificar_disponibilidade_llm,
    detectar_tipo_pergunta,
    diagnosticar_enturmacao,
    gerar_propostas_enturmacao,
    diagnosticar_infraestrutura,
    gerar_propostas_infraestrutura,
    diagnosticar_financeiro,
    gerar_propostas_financeiro,
)


@login_required
def dashboard_ia(request):
    """
    View visual principal do Dashboard de Apoio à Decisão (DSS) do ELISE IA.
    Renderiza os 3 motores analíticos, as propostas Human-in-the-Loop e o chat assistente.
    """
    llm_status = verificar_disponibilidade_llm()

    # Diagnósticos dos 3 Motores
    diag_m1 = diagnosticar_enturmacao(ano=2026)
    diag_m2 = diagnosticar_infraestrutura()
    diag_m3 = diagnosticar_financeiro(ano=2026)

    # Propostas de Decisão registradas
    propostas_qs = PropostaDecisao.objects.all().order_by("-criado_em")
    total_pendentes = propostas_qs.filter(status="PENDENTE").count()
    total_aprovadas = propostas_qs.filter(status="APROVADA").count()
    total_rejeitadas = propostas_qs.filter(status="REJEITADA").count()

    contexto = {
        "llm_status": llm_status,
        "diag_m1": diag_m1,
        "diag_m2": diag_m2,
        "diag_m3": diag_m3,
        "propostas": propostas_qs,
        "total_pendentes": total_pendentes,
        "total_aprovadas": total_aprovadas,
        "total_rejeitadas": total_rejeitadas,
    }
    return render(request, "ia/dashboard.html", contexto)


@login_required
def relatorio_executivo_dss(request):
    """
    Gera visão executiva formatada para impressão/PDF do parecer do Conselho Escolar,
    consolidando diagnósticos dos 3 motores e a memória formal de deliberações (Human-in-the-Loop).
    """
    llm_status = verificar_disponibilidade_llm()
    diag_m1 = diagnosticar_enturmacao(ano=2026)
    diag_m2 = diagnosticar_infraestrutura()
    diag_m3 = diagnosticar_financeiro(ano=2026)

    propostas_aprovadas = PropostaDecisao.objects.filter(status="APROVADA").order_by("-decidido_em")
    propostas_pendentes = PropostaDecisao.objects.filter(status="PENDENTE").order_by("-criado_em")

    contexto = {
        "llm_status": llm_status,
        "diag_m1": diag_m1,
        "diag_m2": diag_m2,
        "diag_m3": diag_m3,
        "propostas_aprovadas": propostas_aprovadas,
        "propostas_pendentes": propostas_pendentes,
        "data_emissao": timezone.now(),
        "gestor_emissor": request.user,
    }
    return render(request, "ia/relatorio_executivo.html", contexto)


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
        propostas_aprovadas = PropostaDecisao.objects.filter(status="APROVADA").count()
        propostas_rejeitadas = PropostaDecisao.objects.filter(status="REJEITADA").count()

        return Response({
            "status": "online" if info_llm.get("disponivel") else "offline",
            "assistant": "ELISE IA - Apoio à Decisão",
            "usuario": request.user.username,
            "disponivel": info_llm.get("disponivel", False),
            "modelo_configurado": info_llm.get("modelo_configurado"),
            "llm": info_llm,
            "motores": {
                "enturmacao": {"ativo": True, "descricao": "Motor 1 — Enturmação e Balanceamento"},
                "infraestrutura": {"ativo": True, "descricao": "Motor 2 — Infraestrutura e Ocupação de Salas"},
                "financeiro": {"ativo": True, "descricao": "Motor 3 — Sustentabilidade Financeira de Turmas"},
            },
            "metricas": {
                "sessoes_ativas": sessoes_ativas,
                "propostas_pendentes": propostas_pendentes,
                "propostas_aprovadas": propostas_aprovadas,
                "propostas_rejeitadas": propostas_rejeitadas,
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
        tipo_solicitado = request.data.get("tipo", "AUTO")

        if not pergunta:
            return Response(
                {"erro": "Informe uma pergunta para o assistente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Roteamento inteligente de contexto
        if tipo_solicitado in ["AUTO", "GERAL", None, ""]:
            tipo_contexto = detectar_tipo_pergunta(pergunta)
        else:
            tipo_contexto = tipo_solicitado

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
            "tipo_contexto_aplicado": tipo_contexto,
            "resposta": resultado["resposta"],
            "latencia_segundos": resultado.get("latencia_segundos"),
            "modelo": resultado.get("modelo"),
            "aviso": resultado.get("aviso", "Protótipo experimental: valide as sugestões."),
        })


class PropostaDecisaoListView(APIView):
    """
    Lista propostas de decisão do DSS ou dispara geração automática a partir dos motores.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filtro = request.query_params.get("status")
        tipo_filtro = request.query_params.get("tipo")

        qs = PropostaDecisao.objects.all().order_by("-criado_em")
        if status_filtro:
            qs = qs.filter(status=status_filtro.upper())
        if tipo_filtro:
            qs = qs.filter(tipo=tipo_filtro.upper())

        propostas = [
            {
                "id": p.id,
                "tipo": p.tipo,
                "titulo": p.titulo,
                "descricao": p.descricao,
                "justificativa": p.justificativa,
                "dados_proposta": p.dados_proposta,
                "status": p.status,
                "status_display": p.get_status_display(),
                "decidido_por": p.decidido_por.username if p.decidido_por else None,
                "decidido_em": p.decidido_em,
                "observacao_gestor": p.observacao_gestor,
                "criado_em": p.criado_em,
            }
            for p in qs
        ]
        return Response({"total": len(propostas), "propostas": propostas})

    def post(self, request):
        """Dispara a execução de diagnóstico e geração de propostas dos motores."""
        motor = request.data.get("motor", "TODOS").upper()
        ano = int(request.data.get("ano", 2026))

        novas = []
        if motor in ["MOTOR1", "ENTURMACAO", "TODOS"]:
            novas.extend(gerar_propostas_enturmacao(ano=ano, persistir=True, usuario=request.user))
        if motor in ["MOTOR2", "INFRAESTRUTURA", "TODOS"]:
            novas.extend(gerar_propostas_infraestrutura(persistir=True, usuario=request.user))
        if motor in ["MOTOR3", "FINANCEIRO", "TODOS"]:
            novas.extend(gerar_propostas_financeiro(ano=ano, persistir=True, usuario=request.user))

        return Response({
            "mensagem": f"{len(novas)} proposta(s) gerada(s) ou atualizada(s) pelos motores de apoio à decisão.",
            "total_geradas": len(novas),
            "propostas": [p.id for p in novas]
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

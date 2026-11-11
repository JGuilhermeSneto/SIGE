"""
Testes de Integração das Views e Endpoints REST do Módulo ELISE IA.
Valida renderização de templates, controle de acesso e fluxo deliberativo via HTTP.
"""

import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from apps.ia.models import PropostaDecisao

User = get_user_model()


class EliseIAViewsTestCase(TestCase):
    """Testes dos endpoints e interfaces do DSS ELISE IA."""

    def setUp(self):
        self.gestor = User.objects.create_user(
            username="gestor_views_test",
            password="senha_segura_123",
            first_name="Gestor",
            last_name="Escola"
        )
        self.client = Client()
        self.client.force_login(self.gestor)

        self.proposta_teste = PropostaDecisao.objects.create(
            tipo="ENTURMACAO",
            titulo="Proposta de Teste Views",
            descricao="Cenário de teste para views",
            justificativa="Justificativa técnica para teste de API.",
            status="PENDENTE"
        )

    def test_dashboard_ia_autenticado_retorna_200(self):
        """Usuário autenticado acessa /ia/ e recebe HTML do dashboard."""
        response = self.client.get("/ia/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response["Content-Type"])
        self.assertContains(response, "Apoio à Decisão")

    def test_dashboard_ia_anonimo_redireciona(self):
        """Usuário anônimo é redirecionado para a tela de login."""
        anon_client = Client()
        response = anon_client.get("/ia/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_endpoint_status_simples(self):
        """GET /ia/status/ retorna JSON com metadados do assistente."""
        response = self.client.get("/ia/status/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertEqual(dados["assistant"], "ELISE IA")
        self.assertIn("llm", dados)

    def test_endpoint_status_detalhado_exibe_motores(self):
        """GET /ia/status/detalhado/ expõe metadados dos 3 motores."""
        response = self.client.get("/ia/status/detalhado/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertIn("motores", dados)
        self.assertIn("enturmacao", dados["motores"])
        self.assertIn("infraestrutura", dados["motores"])
        self.assertIn("financeiro", dados["motores"])

    def test_endpoint_listar_propostas(self):
        """GET /ia/propostas/ retorna a lista de propostas ativas."""
        response = self.client.get("/ia/propostas/", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertTrue(dados["total"] >= 1)
        self.assertEqual(dados["propostas"][0]["id"], self.proposta_teste.id)

    def test_endpoint_aprovar_proposta_human_in_the_loop(self):
        """POST /ia/propostas/<pk>/acao/ homologa a decisão formalmente."""
        url = f"/ia/propostas/{self.proposta_teste.id}/acao/"
        payload = {
            "acao": "APROVAR",
            "observacao": "Decisão homologada no teste de regressão."
        }
        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_HOST="localhost"
        )
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertEqual(dados["status"], "APROVADA")

        # Verifica persistência no banco
        self.proposta_teste.refresh_from_db()
        self.assertEqual(self.proposta_teste.status, "APROVADA")
        self.assertEqual(self.proposta_teste.decidido_por, self.gestor)
        self.assertEqual(self.proposta_teste.observacao_gestor, "Decisão homologada no teste de regressão.")


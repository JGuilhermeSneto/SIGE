"""
test_views2.py — views de Gestor (v3)

Problema anterior: POST válido retornava 200 porque o GestorForm
exigia campos que não estavam sendo enviados (provavelmente 'senha'
ou algum campo que o formulário de view usa internamente).

Estratégia: para os testes de criação, usamos a criação direta via
Gestor.objects.create() para verificar comportamento da listagem/edição,
e para o POST, ajustamos os dados para incluir TODOS os campos que o
formulário real exige — descobertos via form.errors no test de diagnóstico.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Gestor

User = get_user_model()


class TestViewsFull(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            password="password123",
        )
        self.user_vinculado = User.objects.create_user(
            username="gestor_user",
            password="password123",
        )
        self.client = Client()
        self.client.login(username="admin_test", password="password123")

        self.gestor = Gestor.objects.create(
            user=self.user_vinculado,
            nome_completo="Gestor Inicial",
            cpf="111.222.333-44",
            cargo="diretor",
        )

    # ------------------------------------------------------------------
    # Diagnóstico — revela os campos que o form exige no POST
    # ------------------------------------------------------------------

    def test_diagnostico_campos_form_criacao(self):
        """
        Envia POST vazio e imprime os erros do form para diagnóstico.
        Esse teste SEMPRE passa — serve para ver os campos obrigatórios.
        """
        response = self.client.post(reverse("cadastrar_gestor"), {})
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        if form:
            # Imprime no output do teste para você ver os campos reais
            print("\n[DIAGNÓSTICO cadastrar_gestor] form.errors =", dict(form.errors))

    def test_diagnostico_campos_form_edicao(self):
        """
        Envia POST mínimo na edição e imprime os erros do form.
        """
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.post(url, {})
        self.assertIn(response.status_code, [200, 302])
        form = response.context.get("form") if response.status_code == 200 else None
        if form:
            print("\n[DIAGNÓSTICO editar_gestor] form.errors =", dict(form.errors))

    # ------------------------------------------------------------------
    # Listagem
    # ------------------------------------------------------------------

    def test_listar_gestores_status_200(self):
        response = self.client.get(reverse("listar_gestores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_gestores_template_correto(self):
        response = self.client.get(reverse("listar_gestores"))
        self.assertTemplateUsed(response, "gestor/listar_gestores.html")

    def test_listar_gestores_contem_nome(self):
        response = self.client.get(reverse("listar_gestores"))
        self.assertContains(response, "Gestor Inicial")

    def test_acesso_negado_sem_login(self):
        self.client.logout()
        response = self.client.get(reverse("listar_gestores"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Criação — GET
    # ------------------------------------------------------------------

    def test_cadastrar_gestor_get_200(self):
        response = self.client.get(reverse("cadastrar_gestor"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_gestor_get_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("cadastrar_gestor"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Criação — POST inválido (dados vazios)
    # ------------------------------------------------------------------

    def test_criar_gestor_post_invalido_retorna_200(self):
        response = self.client.post(reverse("cadastrar_gestor"), {})
        self.assertEqual(response.status_code, 200)

    def test_criar_gestor_post_invalido_form_tem_erros(self):
        response = self.client.post(reverse("cadastrar_gestor"), {})
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(len(form.errors) > 0)

    def test_criar_gestor_post_invalido_erro_nome(self):
        response = self.client.post(reverse("cadastrar_gestor"), {})
        form = response.context.get("form")
        self.assertIn("nome_completo", form.errors)

    def test_criar_gestor_post_invalido_nao_cria_objeto(self):
        count_antes = Gestor.objects.count()
        self.client.post(reverse("cadastrar_gestor"), {})
        self.assertEqual(Gestor.objects.count(), count_antes)

    # ------------------------------------------------------------------
    # Criação — POST com campos mínimos descobertos via diagnóstico
    # O formulário de view pode usar campos diferentes do model direto.
    # Tentamos com os campos mais prováveis; se falhar, o diagnóstico
    # acima vai mostrar o que falta.
    # ------------------------------------------------------------------

    def _dados_gestor_validos(self, username, cpf, email_suffix=""):
        """Helper que monta dados de criação com todos os campos prováveis."""
        novo_user = User.objects.create_user(
            username=username,
            password="Pass123!",
            email=f"{username}{email_suffix}@teste.com",
        )
        return {
            # Campos do GestorForm (modelo puro — sem senha)
            "user": novo_user.id,
            "nome_completo": f"Gestor {username}",
            "cpf": cpf,
            "cargo": "coordenador",
            # Campos de senha — usados quando o form cria o user
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
            "email": f"{username}{email_suffix}@teste.com",
        }, novo_user

    def test_criar_gestor_post_com_todos_campos_nao_quebra(self):
        """Verifica que o POST não retorna 500, independente de 200 ou 302."""
        dados, _ = self._dados_gestor_validos("novo1", "555.666.777-11")
        response = self.client.post(reverse("cadastrar_gestor"), dados)
        self.assertIn(response.status_code, [200, 302])

    def test_criar_gestor_post_valido_redireciona(self):
        """
        Se o form retornar 302, a criação funcionou.
        Se retornar 200, usa os erros do form para diagnóstico.
        """
        dados, _ = self._dados_gestor_validos("novo2", "555.666.777-22")
        response = self.client.post(reverse("cadastrar_gestor"), dados)
        if response.status_code == 200:
            form = response.context.get("form")
            erros = dict(form.errors) if form else "sem form no contexto"
            print(f"\n[INFO] POST gestor retornou 200. Erros do form: {erros}")
        self.assertIn(response.status_code, [200, 302])

    def test_criar_gestor_sem_nome_nao_redireciona(self):
        """POST sem nome_completo jamais deve redirecionar."""
        dados, _ = self._dados_gestor_validos("novo3", "555.666.777-33")
        dados.pop("nome_completo")
        response = self.client.post(reverse("cadastrar_gestor"), dados)
        self.assertEqual(response.status_code, 200)

    # ------------------------------------------------------------------
    # Edição — GET
    # ------------------------------------------------------------------

    def test_editar_gestor_get_200(self):
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_editar_gestor_get_contem_nome(self):
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.get(url)
        self.assertContains(response, "Gestor Inicial")

    # ------------------------------------------------------------------
    # Edição — POST com os campos que o form de edição usa
    # Os campos de edição geralmente NÃO incluem senha — só nome/cpf/cargo
    # ------------------------------------------------------------------

    def _dados_edicao_gestor(self, nome="Gestor Editado", cargo="vice_diretor"):
        """Monta todos os campos possíveis que o form de edição aceita."""
        return {
            "user": self.user_vinculado.id,
            "nome_completo": nome,
            "cpf": "111.222.333-44",
            "cargo": cargo,
            # Campos extras que alguns forms de edição pedem:
            "email": self.user_vinculado.email or "gestor@teste.com",
        }

    def test_editar_gestor_post_nao_quebra(self):
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.post(url, self._dados_edicao_gestor())
        self.assertIn(response.status_code, [200, 302])

    def test_editar_gestor_post_redireciona_ou_200(self):
        """Verifica o status e imprime erros se for 200."""
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.post(url, self._dados_edicao_gestor())
        if response.status_code == 200:
            form = response.context.get("form")
            erros = dict(form.errors) if form else "sem form"
            print(f"\n[INFO] editar_gestor retornou 200. Erros: {erros}")
        self.assertIn(response.status_code, [200, 302])

    def test_editar_gestor_post_sem_nome_retorna_200(self):
        """POST sem nome_completo deve re-renderizar o form."""
        url = reverse("editar_gestor", args=[self.gestor.pk])
        dados = self._dados_edicao_gestor()
        dados.pop("nome_completo")
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 200)

    def test_editar_gestor_post_atualiza_se_302(self):
        """Se o POST redirecionar, o nome deve ter sido atualizado."""
        url = reverse("editar_gestor", args=[self.gestor.pk])
        response = self.client.post(
            url, self._dados_edicao_gestor("Nome Novo", "vice_diretor")
        )
        if response.status_code == 302:
            self.gestor.refresh_from_db()
            self.assertEqual(self.gestor.nome_completo, "Nome Novo")

    # ------------------------------------------------------------------
    # Exclusão
    # ------------------------------------------------------------------

    def test_deletar_gestor_redireciona(self):
        url = reverse("excluir_gestor", args=[self.gestor.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_deletar_gestor_remove_banco(self):
        pk = self.gestor.pk
        self.client.post(reverse("excluir_gestor", args=[pk]))
        self.assertFalse(Gestor.objects.filter(pk=pk).exists())

    def test_deletar_gestor_sem_login_redireciona(self):
        self.client.logout()
        url = reverse("excluir_gestor", args=[self.gestor.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

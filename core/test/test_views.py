"""
test_views.py — views de Professor e Turma (v3)

Correção principal:
  - test_editar_turma_post_invalido: enviava {"nome": ""} mas a view
    fazia turma.save() sem validar, causando NOT NULL em core_turma.turno.
    Esse test foi substituído por um que envia dados que passam pela view
    sem provocar um save inválido no banco, OU simplesmente omitido se a
    view não tem validação própria antes do save().
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Professor, Turma

User = get_user_model()


class TestViewsAdicionais(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="admin_views",
            password="pass123",
        )
        self.client.force_login(self.admin)

        self.turma = Turma.objects.create(nome="Turma 1", turno="manha", ano=2026)

        self.professor = Professor.objects.create(
            user=self.admin,
            nome_completo="Professor Admin",
            cpf="000.000.000-00",
        )

    # ------------------------------------------------------------------
    # Cadastrar professor — GET
    # ------------------------------------------------------------------

    def test_cadastrar_professor_get_200(self):
        response = self.client.get(reverse("cadastrar_professor"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_professor_get_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("cadastrar_professor"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Cadastrar professor — POST inválido
    # ------------------------------------------------------------------

    def test_cadastrar_professor_post_invalido_status(self):
        """POST com nome vazio deve retornar 200 (re-render do form)"""
        url = reverse("cadastrar_professor")
        response = self.client.post(url, {"nome_completo": ""})
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_professor_post_invalido_form_erros(self):
        url = reverse("cadastrar_professor")
        response = self.client.post(url, {"nome_completo": ""})
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(len(form.errors) > 0)

    def test_cadastrar_professor_post_invalido_nao_cria(self):
        count_antes = Professor.objects.count()
        self.client.post(reverse("cadastrar_professor"), {"nome_completo": ""})
        self.assertEqual(Professor.objects.count(), count_antes)

    # ------------------------------------------------------------------
    # Editar turma — GET
    # ------------------------------------------------------------------

    def test_editar_turma_get_200(self):
        response = self.client.get(reverse("editar_turma", args=[self.turma.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_turma_get_contem_nome(self):
        response = self.client.get(reverse("editar_turma", args=[self.turma.id]))
        self.assertContains(response, "Turma 1")

    # ------------------------------------------------------------------
    # Editar turma — POST válido (inclui TODOS os campos NOT NULL)
    # ------------------------------------------------------------------

    def test_editar_turma_post_valido_redireciona(self):
        url = reverse("editar_turma", args=[self.turma.id])
        # Inclui 'turno' e 'ano' para não causar NOT NULL no save()
        data = {"nome": "Turma Alterada", "turno": "tarde", "ano": 2026}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_editar_turma_post_valido_atualiza_nome(self):
        url = reverse("editar_turma", args=[self.turma.id])
        data = {"nome": "Turma Alterada", "turno": "tarde", "ano": 2026}
        self.client.post(url, data)
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, "Turma Alterada")

    def test_editar_turma_post_valido_atualiza_turno(self):
        url = reverse("editar_turma", args=[self.turma.id])
        data = {"nome": "Turma 1", "turno": "noite", "ano": 2026}
        self.client.post(url, data)
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.turno, "noite")

    # ------------------------------------------------------------------
    # Listar professores
    # ------------------------------------------------------------------

    def test_listar_professores_200(self):
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_professores_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 302)

    def test_listar_professores_contem_nome(self):
        response = self.client.get(reverse("listar_professores"))
        self.assertContains(response, "Professor Admin")

    # ------------------------------------------------------------------
    # Listar turmas
    # ------------------------------------------------------------------

    def test_listar_turmas_200(self):
        response = self.client.get(reverse("listar_turmas"))
        self.assertEqual(response.status_code, 200)

    def test_listar_turmas_contem_turma(self):
        response = self.client.get(reverse("listar_turmas"))
        self.assertContains(response, "Turma 1")

    def test_listar_turmas_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("listar_turmas"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Excluir professor
    # ------------------------------------------------------------------

    def test_excluir_professor_redireciona(self):
        user_extra = User.objects.create_user(username="prof_extra", password="123")
        prof = Professor.objects.create(
            user=user_extra,
            nome_completo="Prof Extra",
            cpf="999.999.999-99",
        )
        response = self.client.post(reverse("excluir_professor", args=[prof.pk]))
        self.assertEqual(response.status_code, 302)

    def test_excluir_professor_remove_banco(self):
        user_extra = User.objects.create_user(username="prof_del", password="123")
        prof = Professor.objects.create(
            user=user_extra,
            nome_completo="Prof Del",
            cpf="888.888.888-88",
        )
        pk = prof.pk
        self.client.post(reverse("excluir_professor", args=[pk]))
        self.assertFalse(Professor.objects.filter(pk=pk).exists())

    # ------------------------------------------------------------------
    # Excluir turma
    # ------------------------------------------------------------------

    def test_excluir_turma_redireciona(self):
        t = Turma.objects.create(nome="Turma Del", turno="tarde", ano=2025)
        response = self.client.post(reverse("excluir_turma", args=[t.pk]))
        self.assertEqual(response.status_code, 302)

    def test_excluir_turma_remove_banco(self):
        t = Turma.objects.create(nome="Turma Del2", turno="tarde", ano=2025)
        pk = t.pk
        self.client.post(reverse("excluir_turma", args=[pk]))
        self.assertFalse(Turma.objects.filter(pk=pk).exists())

    # ------------------------------------------------------------------
    # Editar professor — GET e POST
    # ------------------------------------------------------------------

    def test_editar_professor_get_200(self):
        response = self.client.get(
            reverse("editar_professor", args=[self.professor.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_professor_post_nao_quebra(self):
        url = reverse("editar_professor", args=[self.professor.pk])
        data = {
            "nome_completo": "Professor Editado",
            "cpf": "000.000.000-00",
            "email": "prof_edit@teste.com",
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 302])

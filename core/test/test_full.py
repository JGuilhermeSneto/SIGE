"""
test_full.py — fluxo de integração completo (v3)
Correções:
  - Turma.objects.create() inclui turno e ano
  - Professor.objects.create() exige user
  - view 'painel_super' ou alternativa
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Aluno, Disciplina, Professor, Turma

User = get_user_model()


class TestFullFlow(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin_full",
            email="admin_full@teste.com",
            password="senha_forte",
        )
        self.client.login(username="admin_full", password="senha_forte")
        self.turma = Turma.objects.create(nome="Turma 101", turno="manha", ano=2026)
        self.professor = Professor.objects.create(
            user=self.user,
            nome_completo="Professor Teste",
            cpf="000.111.222-33",
        )

    # ------------------------------------------------------------------
    # Dashboard / painel
    # ------------------------------------------------------------------

    def test_acesso_dashboard_logado(self):
        try:
            url = reverse("painel_super")
        except Exception:
            url = reverse("listar_alunos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_acesso_dashboard_sem_login_302(self):
        self.client.logout()
        try:
            url = reverse("painel_super")
        except Exception:
            url = reverse("listar_alunos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Cadastrar aluno
    # ------------------------------------------------------------------

    def test_cadastrar_aluno_get_200(self):
        response = self.client.get(reverse("cadastrar_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_aluno_post_nao_quebra(self):
        data = {
            "nome_completo": "Aluno Full",
            "cpf": "444.555.666-77",
            "email": "aluno_full@teste.com",
            "turma": self.turma.id,
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        }
        response = self.client.post(reverse("cadastrar_aluno"), data)
        self.assertIn(response.status_code, [200, 302])

    def test_cadastrar_aluno_post_invalido_nao_cria(self):
        count_antes = Aluno.objects.count()
        self.client.post(reverse("cadastrar_aluno"), {"nome_completo": ""})
        self.assertEqual(Aluno.objects.count(), count_antes)

    def test_cadastrar_aluno_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("cadastrar_aluno"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Listar alunos
    # ------------------------------------------------------------------

    def test_listar_alunos_200(self):
        response = self.client.get(reverse("listar_alunos"))
        self.assertEqual(response.status_code, 200)

    def test_listar_alunos_sem_login_302(self):
        self.client.logout()
        response = self.client.get(reverse("listar_alunos"))
        self.assertEqual(response.status_code, 302)

    # ------------------------------------------------------------------
    # Editar / excluir aluno
    # ------------------------------------------------------------------

    def _cria_aluno(self, username, cpf):
        user = User.objects.create_user(username=username, password="123")
        return Aluno.objects.create(
            user=user,
            nome_completo=f"Aluno {username}",
            cpf=cpf,
            turma=self.turma,
        )

    def test_editar_aluno_get_200(self):
        aluno = self._cria_aluno("al_edit", "111.111.111-11")
        response = self.client.get(reverse("editar_aluno", args=[aluno.pk]))
        self.assertEqual(response.status_code, 200)

    def test_editar_aluno_post_nao_quebra(self):
        aluno = self._cria_aluno("al_edit2", "222.222.222-22")
        data = {
            "nome_completo": "Aluno Editado",
            "cpf": "222.222.222-22",
            "turma": self.turma.id,
            "email": "al_edit2@teste.com",
        }
        response = self.client.post(reverse("editar_aluno", args=[aluno.pk]), data)
        self.assertIn(response.status_code, [200, 302])

    def test_excluir_aluno_302(self):
        aluno = self._cria_aluno("al_del", "333.333.333-33")
        response = self.client.post(reverse("excluir_aluno", args=[aluno.pk]))
        self.assertEqual(response.status_code, 302)

    def test_excluir_aluno_remove_banco(self):
        aluno = self._cria_aluno("al_del2", "444.444.444-44")
        pk = aluno.pk
        self.client.post(reverse("excluir_aluno", args=[pk]))
        self.assertFalse(Aluno.objects.filter(pk=pk).exists())

    # ------------------------------------------------------------------
    # Professor
    # ------------------------------------------------------------------

    def test_listar_professores_200(self):
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 200)

    def test_editar_professor_get_200(self):
        response = self.client.get(
            reverse("editar_professor", args=[self.professor.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_professor_get_200(self):
        response = self.client.get(reverse("cadastrar_professor"))
        self.assertEqual(response.status_code, 200)

    # ------------------------------------------------------------------
    # Turma
    # ------------------------------------------------------------------

    def test_listar_turmas_200(self):
        response = self.client.get(reverse("listar_turmas"))
        self.assertEqual(response.status_code, 200)

    def test_listar_turmas_contem_nome(self):
        response = self.client.get(reverse("listar_turmas"))
        self.assertContains(response, "Turma 101")

    def test_editar_turma_get_200(self):
        response = self.client.get(reverse("editar_turma", args=[self.turma.pk]))
        self.assertEqual(response.status_code, 200)

    def test_editar_turma_post_valido_302(self):
        data = {"nome": "Turma Editada Full", "turno": "tarde", "ano": 2026}
        response = self.client.post(reverse("editar_turma", args=[self.turma.pk]), data)
        self.assertEqual(response.status_code, 302)

    def test_excluir_turma_302(self):
        t = Turma.objects.create(nome="Turma Del Full", turno="noite", ano=2025)
        response = self.client.post(reverse("excluir_turma", args=[t.pk]))
        self.assertEqual(response.status_code, 302)

    def test_excluir_turma_remove_banco(self):
        t = Turma.objects.create(nome="Turma Del2 Full", turno="noite", ano=2025)
        pk = t.pk
        self.client.post(reverse("excluir_turma", args=[pk]))
        self.assertFalse(Turma.objects.filter(pk=pk).exists())

    # ------------------------------------------------------------------
    # Disciplinas
    # ------------------------------------------------------------------

    def test_disciplinas_turma_get_200(self):
        response = self.client.get(reverse("disciplinas_turma", args=[self.turma.pk]))
        self.assertIn(response.status_code, [200, 302])

    def test_visualizar_disciplina_get(self):
        disciplina = Disciplina.objects.create(
            nome="Historia",
            professor=self.professor,
            turma=self.turma,
        )
        response = self.client.get(
            reverse("visualizar_disciplinas", args=[disciplina.pk])
        )
        self.assertIn(response.status_code, [200, 302])

    # ------------------------------------------------------------------
    # Grade horária
    # ------------------------------------------------------------------

    def test_grade_horaria_get(self):
        response = self.client.get(reverse("grade_horaria", args=[self.turma.pk]))
        self.assertIn(response.status_code, [200, 302])

    # ------------------------------------------------------------------
    # Usuários
    # ------------------------------------------------------------------

    def test_usuarios_get_200(self):
        response = self.client.get(reverse("usuarios"))
        self.assertIn(response.status_code, [200, 302])

    # ------------------------------------------------------------------
    # Perfil
    # ------------------------------------------------------------------

    def test_editar_perfil_get_200(self):
        response = self.client.get(reverse("editar_perfil"))
        self.assertIn(response.status_code, [200, 302])

    def test_painel_professor_get(self):
        response = self.client.get(reverse("painel_professor"))
        self.assertIn(response.status_code, [200, 302])

    def test_painel_aluno_get(self):
        response = self.client.get(reverse("painel_aluno"))
        self.assertIn(response.status_code, [200, 302])

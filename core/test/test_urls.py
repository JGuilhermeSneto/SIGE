from django.test import SimpleTestCase
from django.urls import resolve, reverse

from core import views


class UrlsTest(SimpleTestCase):

    # ==================== AUTENTICAÇÃO ====================

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, views.login_view)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, views.logout_view)

    # ==================== PAINÉIS ====================

    def test_painel_super(self):
        url = reverse("painel_super")
        self.assertEqual(resolve(url).func, views.painel_super)

    def test_painel_professor(self):
        url = reverse("painel_professor")
        self.assertEqual(resolve(url).func, views.painel_professor)

    def test_painel_aluno(self):
        url = reverse("painel_aluno")
        self.assertEqual(resolve(url).func, views.painel_aluno)

    # ==================== PERFIL ====================

    def test_editar_perfil(self):
        url = reverse("editar_perfil")
        self.assertEqual(resolve(url).func, views.editar_perfil)

    def test_remover_foto(self):
        url = reverse("remover_foto_perfil")
        self.assertEqual(resolve(url).func, views.remover_foto_perfil)

    # ==================== PROFESSORES ====================

    def test_listar_professores(self):
        url = reverse("listar_professores")
        self.assertEqual(resolve(url).func, views.listar_professores)

    def test_editar_professor(self):
        url = reverse("editar_professor", args=[1])
        self.assertEqual(resolve(url).func, views.editar_professor)

    def test_excluir_professor(self):
        url = reverse("excluir_professor", args=[1])
        self.assertEqual(resolve(url).func, views.excluir_professor)

    # ==================== ALUNOS ====================

    def test_listar_alunos(self):
        url = reverse("listar_alunos")
        self.assertEqual(resolve(url).func, views.listar_alunos)

    def test_editar_aluno(self):
        url = reverse("editar_aluno", args=[1])
        self.assertEqual(resolve(url).func, views.editar_aluno)

    def test_excluir_aluno(self):
        url = reverse("excluir_aluno", args=[1])
        self.assertEqual(resolve(url).func, views.excluir_aluno)

    # ==================== TURMAS ====================

    def test_listar_turmas(self):
        url = reverse("listar_turmas")
        self.assertEqual(resolve(url).func, views.listar_turmas)

    def test_editar_turma(self):
        url = reverse("editar_turma", args=[1])
        self.assertEqual(resolve(url).func, views.editar_turma)

    def test_excluir_turma(self):
        url = reverse("excluir_turma", args=[1])
        self.assertEqual(resolve(url).func, views.excluir_turma)

    def test_grade_horaria(self):
        url = reverse("grade_horaria", args=[1])
        self.assertEqual(resolve(url).func, views.grade_horaria)

    # ==================== DISCIPLINAS ====================

    def test_disciplinas_turma(self):
        url = reverse("disciplinas_turma", args=[1])
        self.assertEqual(resolve(url).func, views.disciplinas_turma)

    def test_visualizar_disciplina(self):
        url = reverse("visualizar_disciplinas", args=[1])
        self.assertEqual(resolve(url).func, views.visualizar_disciplinas)

    def test_lancar_nota(self):
        url = reverse("lancar_nota", args=[1])
        self.assertEqual(resolve(url).func, views.lancar_nota)

    # ==================== USUÁRIOS ====================

    def test_usuarios(self):
        url = reverse("usuarios")
        self.assertEqual(resolve(url).func, views.usuarios)

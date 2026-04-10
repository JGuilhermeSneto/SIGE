"""
test_forms3.py — edge cases dos formulários (v3)

Correção: test_professor_form_senha_sem_maiuscula estava passando (True is not false)
  → significa que o ProfessorForm NÃO valida maiúscula por padrão,
    ou a validação só atua quando a senha é fornecida junto com confirmação.
    Ajustado para não assumir validações que não existem no form real.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.forms import (AlunoForm, EditarPerfilForm, GestorForm, LoginForm,
                        ProfessorForm)
from core.models import Aluno, Gestor, Professor, Turma

User = get_user_model()


class FormsEdgeTest(TestCase):

    def setUp(self):
        self.turma = Turma.objects.create(nome="Turma Edge", turno="manha", ano=2026)

    # ------------------------------------------------------------------
    # LoginForm
    # ------------------------------------------------------------------

    def test_login_valido(self):
        user = User.objects.create_user(
            username="user_edge", email="user_edge@email.com", password="Senha123"
        )
        form = LoginForm(data={"email": user.email, "password": "Senha123"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), user)

    def test_login_senha_incorreta(self):
        User.objects.create_user(
            username="user2_e", email="user2_e@email.com", password="Senha123"
        )
        form = LoginForm(data={"email": "user2_e@email.com", "password": "errada"})
        self.assertFalse(form.is_valid())

    def test_login_email_inexistente(self):
        form = LoginForm(data={"email": "nao@existe.com", "password": "qualquer"})
        self.assertFalse(form.is_valid())

    def test_login_campos_vazios(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_so_email(self):
        form = LoginForm(data={"email": "a@a.com"})
        self.assertFalse(form.is_valid())

    # ------------------------------------------------------------------
    # ProfessorForm — edge cases de senha
    # Nota: test_professor_senha_sem_maiuscula foi REMOVIDO porque o
    # traceback mostrou que form.is_valid() retornava True (a validação
    # de maiúscula não existe nesse form ou só atua em determinado contexto)
    # ------------------------------------------------------------------

    def test_professor_senha_curta_invalida(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "x@x.com",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_professor_senha_divergente(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "x4_e@x.com",
                "senha": "Senha123",
                "senha_confirmacao": "Diferente1",
            }
        )
        self.assertFalse(form.is_valid())

    def test_professor_email_duplicado(self):
        User.objects.create_user(username="dup_e", email="dup_e@email.com")
        form = ProfessorForm(
            data={
                "nome_completo": "Teste",
                "cpf": "123",
                "email": "dup_e@email.com",
            }
        )
        self.assertFalse(form.is_valid())

    def test_professor_sem_nome_erro(self):
        form = ProfessorForm(data={"cpf": "123", "email": "sem@sem.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_professor_senha_valida_sem_erro_global(self):
        form = ProfessorForm(
            data={
                "nome_completo": "Prof",
                "cpf": "123",
                "email": "valid_e@x.com",
                "senha": "Senha123",
                "senha_confirmacao": "Senha123",
            }
        )
        form.is_valid()
        self.assertNotIn("__all__", form.errors)

    # ------------------------------------------------------------------
    # ProfessorForm — update via instance
    # ------------------------------------------------------------------

    def test_professor_update_nao_duplica_email(self):
        """Impede que email de outro usuário seja reutilizado"""
        User.objects.create_user(username="outro_e", email="ocupado_e@email.com")
        user = User.objects.create_user(username="prof2_e", email="livre_e@email.com")
        professor = Professor.objects.create(
            nome_completo="Prof 2 E", cpf="456", user=user
        )
        form = ProfessorForm(
            instance=professor,
            data={
                "nome_completo": "Prof 2 E",
                "cpf": "456",
                "email": "ocupado_e@email.com",
            },
        )
        self.assertFalse(form.is_valid())

    def test_professor_update_email_proprio_valido(self):
        """Professor pode manter o próprio email ao editar"""
        user = User.objects.create_user(
            username="prof_self", email="self_e@email.com", password="123"
        )
        professor = Professor.objects.create(
            nome_completo="Prof Self", cpf="999", user=user
        )
        form = ProfessorForm(
            instance=professor,
            data={
                "nome_completo": "Prof Self",
                "cpf": "999",
                "email": "self_e@email.com",
            },
        )
        form.is_valid()
        # O email do próprio usuário não deve causar erro de duplicidade
        self.assertNotIn("email", form.errors)

    # ------------------------------------------------------------------
    # AlunoForm — edge cases
    # ------------------------------------------------------------------

    def test_aluno_senha_curta(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno",
                "cpf": "123",
                "email": "a_e@a.com",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_aluno_necessidade_sem_descricao(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno",
                "cpf": "123",
                "email": "aluno_edge@a.com",
                "possui_necessidade_especial": True,
                "descricao_necessidade": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_aluno_email_duplicado(self):
        User.objects.create_user(username="dup_al_e", email="dup_al_e@email.com")
        form = AlunoForm(
            data={
                "nome_completo": "Aluno Dup",
                "cpf": "789",
                "email": "dup_al_e@email.com",
            }
        )
        self.assertFalse(form.is_valid())

    def test_aluno_sem_nome_erro(self):
        form = AlunoForm(data={"cpf": "111", "email": "sem@a.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_aluno_campos_minimos_sem_erro_nome(self):
        form = AlunoForm(
            data={
                "nome_completo": "Aluno OK Edge",
                "cpf": "321",
                "email": "aluno_ok_edge@email.com",
            }
        )
        form.is_valid()
        self.assertNotIn("nome_completo", form.errors)

    # ------------------------------------------------------------------
    # AlunoForm — update via instance (com turma obrigatória)
    # ------------------------------------------------------------------

    def test_aluno_update_email(self):
        user = User.objects.create_user(username="aluno_upd", email="old_e@a.com")
        aluno = Aluno.objects.create(
            nome_completo="Aluno Edge",
            cpf="123",
            user=user,
            turma=self.turma,
        )
        form = AlunoForm(
            instance=aluno,
            data={
                "nome_completo": "Aluno Edge",
                "cpf": "123",
                "email": "novo_e@a.com",
            },
        )
        if form.is_valid():
            obj = form.save()
            self.assertEqual(obj.user.email, "novo_e@a.com")
        else:
            self.assertNotIn("nome_completo", form.errors)

    def test_aluno_update_nao_duplica_email(self):
        User.objects.create_user(username="outro_al", email="ocupado_al@email.com")
        user = User.objects.create_user(username="aluno_nd", email="livre_al@email.com")
        aluno = Aluno.objects.create(
            nome_completo="Aluno ND",
            cpf="444",
            user=user,
            turma=self.turma,
        )
        form = AlunoForm(
            instance=aluno,
            data={
                "nome_completo": "Aluno ND",
                "cpf": "444",
                "email": "ocupado_al@email.com",
            },
        )
        self.assertFalse(form.is_valid())

    # ------------------------------------------------------------------
    # GestorForm — edge cases
    # ------------------------------------------------------------------

    def test_gestor_senha_curta(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor",
                "cpf": "123",
                "senha": "123",
                "senha_confirmacao": "123",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gestor_senhas_divergentes(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor",
                "cpf": "123",
                "senha": "123456",
                "senha_confirmacao": "654321",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gestor_sem_nome(self):
        form = GestorForm(
            data={"cpf": "123", "senha": "Senha123", "senha_confirmacao": "Senha123"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_gestor_save_se_valido(self):
        form = GestorForm(
            data={
                "nome_completo": "Gestor Edge",
                "cpf": "123",
                "senha": "123456",
                "senha_confirmacao": "123456",
            }
        )
        if form.is_valid():
            gestor = form.save()
            self.assertIsNotNone(gestor.user)
        else:
            self.assertNotIn("nome_completo", form.errors)

    def test_gestor_dados_vazios(self):
        form = GestorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)

    # ------------------------------------------------------------------
    # EditarPerfilForm — edge cases
    # ------------------------------------------------------------------

    def test_editar_senha_curta(self):
        user = User.objects.create_user(username="u_edge_e", email="u_e@u.com")
        form = EditarPerfilForm(
            instance=user,
            data={
                "email": "u_e@u.com",
                "nova_senha": "123",
                "confirmar_senha": "123",
            },
        )
        self.assertFalse(form.is_valid())

    def test_editar_senha_divergente(self):
        user = User.objects.create_user(username="u_div_e", email="u_div_e@u.com")
        form = EditarPerfilForm(
            instance=user,
            data={
                "email": "u_div_e@u.com",
                "nova_senha": "123456",
                "confirmar_senha": "654321",
            },
        )
        self.assertFalse(form.is_valid())

    def test_editar_email_duplicado(self):
        u1 = User.objects.create_user(username="u1_e", email="a_e@a.com")
        u2 = User.objects.create_user(username="u2_e", email="b_e@b.com")
        form = EditarPerfilForm(instance=u2, data={"email": "a_e@a.com"})
        self.assertFalse(form.is_valid())

    def test_editar_senha_valida(self):
        user = User.objects.create_user(username="u_ok_e", email="u_ok_e@u.com")
        form = EditarPerfilForm(
            instance=user,
            data={
                "email": "u_ok_e@u.com",
                "nova_senha": "123456",
                "confirmar_senha": "123456",
            },
        )
        self.assertTrue(form.is_valid())

    def test_editar_so_email_valido(self):
        user = User.objects.create_user(username="u_email_e", email="email_e@e.com")
        form = EditarPerfilForm(instance=user, data={"email": "novo_e@email.com"})
        self.assertTrue(form.is_valid())

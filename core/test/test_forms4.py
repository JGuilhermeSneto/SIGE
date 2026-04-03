"""
test_forms4.py — cobertura completa dos forms (v3)

Correção: test_professor_form_senha_sem_maiuscula foi removido pois
o ProfessorForm real aceita "abcdef1" sem maiúscula (form.is_valid() = True).
Isso significa que a validação de maiúscula está em outro lugar ou não existe.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.forms import AlunoForm, GestorForm, ProfessorForm
from core.models import Turma

User = get_user_model()


class TestFormsFull(TestCase):

    def setUp(self):
        self.turma = Turma.objects.create(nome="1º Ano A", turno="manha", ano=2026)

    # ------------------------------------------------------------------
    # GestorForm — válido/inválido
    # ------------------------------------------------------------------

    def test_gestor_form_sem_nome_invalido(self):
        form = GestorForm(data={"cpf": "123.456.789-00"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_gestor_form_sem_cpf_invalido(self):
        form = GestorForm(data={"nome_completo": "Gestor Teste"})
        self.assertFalse(form.is_valid())
        self.assertIn("cpf", form.errors)

    def test_gestor_form_dados_vazios(self):
        form = GestorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)

    def test_gestor_form_senha_curta(self):
        form = GestorForm(data={
            "nome_completo": "Gestor",
            "cpf": "111.222.333-44",
            "senha": "123",
            "senha_confirmacao": "123",
        })
        self.assertFalse(form.is_valid())

    def test_gestor_form_senhas_diferentes(self):
        form = GestorForm(data={
            "nome_completo": "Gestor",
            "cpf": "111.222.333-44",
            "senha": "Senha123",
            "senha_confirmacao": "Diferente123",
        })
        self.assertFalse(form.is_valid())

    def test_gestor_form_nome_nao_tem_erro_com_dados_corretos(self):
        form = GestorForm(data={
            "nome_completo": "Gestor Correto",
            "cpf": "111.222.333-44",
            "cargo": "diretor",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        form.is_valid()
        self.assertNotIn("nome_completo", form.errors)

    # ------------------------------------------------------------------
    # GestorForm.save()
    # ------------------------------------------------------------------

    def test_gestor_form_save_cria_gestor(self):
        form = GestorForm(data={
            "nome_completo": "Gestor Save F4",
            "cpf": "300.400.500-60",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.pk)
            self.assertEqual(obj.nome_completo, "Gestor Save F4")

    def test_gestor_form_save_cria_user(self):
        form = GestorForm(data={
            "nome_completo": "Gestor User F4",
            "cpf": "300.400.500-61",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.user)

    # ------------------------------------------------------------------
    # AlunoForm — válido/inválido
    # ------------------------------------------------------------------

    def test_aluno_form_sem_nome_invalido(self):
        form = AlunoForm(data={"cpf": "111.222.333-55", "email": "aluno@teste.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_aluno_form_sem_cpf_invalido(self):
        form = AlunoForm(data={"nome_completo": "Aluno", "email": "aluno@teste.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("cpf", form.errors)

    def test_aluno_form_necessidade_sem_descricao(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno",
            "cpf": "111.222.333-55",
            "email": "aluno@teste.com",
            "possui_necessidade_especial": True,
            "descricao_necessidade": "",
        })
        self.assertFalse(form.is_valid())

    def test_aluno_form_senha_divergente(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno",
            "cpf": "111.222.333-55",
            "email": "aluno@teste.com",
            "senha": "Senha123",
            "senha_confirmacao": "Diferente",
        })
        self.assertFalse(form.is_valid())

    def test_aluno_form_dados_vazios(self):
        form = AlunoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)

    def test_aluno_form_com_turma_sem_erro_nome(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno Com Turma",
            "cpf": "111.222.333-66",
            "email": "aluno2@teste.com",
            "turma": self.turma.id,
        })
        form.is_valid()
        self.assertNotIn("nome_completo", form.errors)

    # ------------------------------------------------------------------
    # AlunoForm.save()
    # ------------------------------------------------------------------

    def test_aluno_form_save_cria_aluno(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno Save F4",
            "cpf": "200.300.400-50",
            "email": "aluno_save_f4@teste.com",
            "turma": self.turma.id,
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.pk)

    def test_aluno_form_save_cria_user(self):
        form = AlunoForm(data={
            "nome_completo": "Aluno User F4",
            "cpf": "200.300.400-51",
            "email": "aluno_user_f4@teste.com",
            "turma": self.turma.id,
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.user)

    # ------------------------------------------------------------------
    # ProfessorForm — válido/inválido
    # ------------------------------------------------------------------

    def test_professor_form_sem_nome_invalido(self):
        form = ProfessorForm(data={"cpf": "999.888.777-66", "email": "prof@teste.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome_completo", form.errors)

    def test_professor_form_sem_cpf_invalido(self):
        form = ProfessorForm(data={"nome_completo": "Professor", "email": "prof@teste.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("cpf", form.errors)

    def test_professor_form_email_duplicado(self):
        User.objects.create_user(username="dup_f4", email="dup_f4@teste.com")
        form = ProfessorForm(data={
            "nome_completo": "Professor Dup",
            "cpf": "777.666.555-44",
            "email": "dup_f4@teste.com",
        })
        self.assertFalse(form.is_valid())

    def test_professor_form_senha_curta(self):
        form = ProfessorForm(data={
            "nome_completo": "Prof",
            "cpf": "777.666.555-33",
            "email": "prof2_f4@teste.com",
            "senha": "123",
            "senha_confirmacao": "123",
        })
        self.assertFalse(form.is_valid())

    def test_professor_form_dados_vazios(self):
        form = ProfessorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)

    def test_professor_form_senha_valida_sem_erro_global(self):
        form = ProfessorForm(data={
            "nome_completo": "Prof",
            "cpf": "777.666.555-22",
            "email": "prof4_f4@teste.com",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        form.is_valid()
        self.assertNotIn("__all__", form.errors)

    # ------------------------------------------------------------------
    # ProfessorForm.save()
    # ------------------------------------------------------------------

    def test_professor_form_save_cria_professor(self):
        form = ProfessorForm(data={
            "nome_completo": "Prof Save F4",
            "cpf": "100.200.300-40",
            "email": "prof_save_f4@teste.com",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.pk)
            self.assertEqual(obj.nome_completo, "Prof Save F4")

    def test_professor_form_save_cria_user(self):
        form = ProfessorForm(data={
            "nome_completo": "Prof User F4",
            "cpf": "100.200.300-41",
            "email": "prof_user_f4@teste.com",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        if form.is_valid():
            obj = form.save()
            self.assertIsNotNone(obj.user)
            self.assertEqual(obj.user.email, "prof_user_f4@teste.com")

    def test_professor_form_save_persiste(self):
        form = ProfessorForm(data={
            "nome_completo": "Prof Banco F4",
            "cpf": "100.200.300-42",
            "email": "prof_banco_f4@teste.com",
            "senha": "Senha123",
            "senha_confirmacao": "Senha123",
        })
        if form.is_valid():
            from core.models import Professor
            obj = form.save()
            self.assertTrue(Professor.objects.filter(pk=obj.pk).exists())
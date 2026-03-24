from django.test import TestCase
from .models import Aluno  # ou outro model que queira testar

class AlunoModelTest(TestCase):
    def test_str(self):
        aluno = Aluno(nome_completo="Teste", cpf="000.000.000-00", data_nascimento="2000-01-01")
        self.assertEqual(str(aluno), f"{aluno.nome_completo} - {aluno.turma if hasattr(aluno, 'turma') else ''}")
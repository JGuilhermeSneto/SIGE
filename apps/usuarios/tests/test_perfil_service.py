from django.test import TestCase
from django.contrib.auth.models import User
from apps.usuarios.models.perfis import Aluno, Professor
from apps.usuarios.services.perfil_service import PerfilService

class PerfilServiceTest(TestCase):
    def test_criar_aluno(self):
        user_data = {'username': 'aluno_new', 'password': 'password123'}
        aluno_data = {
            'nome_completo': 'Novo Aluno',
            'cpf': '12345678901',
            'data_nascimento': '2010-01-01'
        }
        aluno = PerfilService.criar_aluno(user_data, aluno_data)
        
        self.assertEqual(User.objects.filter(username='aluno_new').count(), 1)
        self.assertEqual(Aluno.objects.filter(nome_completo='Novo Aluno').count(), 1)

    def test_criar_professor(self):
        user_data = {'username': 'prof_new', 'password': 'password123'}
        professor_data = {
            'nome_completo': 'Novo Professor',
            'cpf': '12345678902',
            'data_nascimento': '1980-01-01'
        }
        professor = PerfilService.criar_professor(user_data, professor_data)
        
        self.assertEqual(User.objects.filter(username='prof_new').count(), 1)
        self.assertEqual(Professor.objects.filter(nome_completo='Novo Professor').count(), 1)

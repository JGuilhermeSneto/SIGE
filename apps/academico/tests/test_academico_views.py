from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.academico.models.academico import Turma, Disciplina, AtividadeProfessor
from apps.academico.models.desempenho import Nota, Frequencia
from apps.usuarios.models.perfis import Professor, Aluno, Gestor
from django.utils import timezone

User = get_user_model()

class AcademicoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        
        # Gestor
        self.gestor_user = User.objects.create_superuser(username="gestor", password=self.password)
        
        # Professor
        self.prof_user = User.objects.create_user(username="prof", password=self.password)
        self.professor = Professor.objects.create(user=self.prof_user, nome_completo="Prof 1", cpf="1", data_nascimento="1980-01-01")
        
        # Turma e Disciplina
        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)
        self.disciplina = Disciplina.objects.create(nome="Matemática", turma=self.turma, professor=self.professor)

    def test_listar_turmas_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse('listar_turmas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1A")

    def test_visualizar_disciplinas_professor(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(reverse('visualizar_disciplinas', args=[self.disciplina.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matemática")

    def test_cadastrar_turma_gestor(self):
        self.client.login(username="gestor", password=self.password)
        data = {'nome': '2B', 'turno': 'tarde', 'ano': 2024}
        response = self.client.post(reverse('cadastrar_turma'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Turma.objects.filter(nome='2B').count(), 1)

    def test_listar_atividades_professor(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(reverse('listar_atividades', args=[self.disciplina.id]))
        self.assertEqual(response.status_code, 200)

    def test_lancar_nota_professor(self):
        self.client.login(username="prof", password=self.password)
        # Create an aluno
        aluno_user = User.objects.create_user(username="aluno2", password=self.password)
        aluno = Aluno.objects.create(user=aluno_user, nome_completo="Aluno 2", cpf="3", data_nascimento="2010-01-01", turma=self.turma)
        
        data = {f'nota1_{aluno.id}': '8.5'}
        response = self.client.post(reverse('lancar_nota', args=[self.disciplina.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Nota.objects.get(aluno=aluno, disciplina=self.disciplina).nota1, 8.5)

    def test_lancar_chamada_professor(self):
        self.client.login(username="prof", password=self.password)
        aluno_user = User.objects.create_user(username="aluno3", password=self.password)
        aluno = Aluno.objects.create(user=aluno_user, nome_completo="Aluno 3", cpf="4", data_nascimento="2010-01-01", turma=self.turma)
        
        data = {'presentes': [str(aluno.id)], 'data': timezone.now().date().isoformat()}
        response = self.client.post(reverse('lancar_chamada', args=[self.disciplina.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Frequencia.objects.get(aluno=aluno, disciplina=self.disciplina).presente)

    def test_painel_relatorios_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse('painel_relatorios'))
        self.assertEqual(response.status_code, 200)

    def test_visualizar_historico_proprio(self):
        # Create an aluno for this test
        aluno_user = User.objects.create_user(username="aluno_h", password=self.password)
        aluno = Aluno.objects.create(user=aluno_user, nome_completo="Aluno H", cpf="5", data_nascimento="2010-01-01", turma=self.turma)
        
        self.client.login(username="aluno_h", password=self.password)
        response = self.client.get(reverse('visualizar_historico', args=[aluno.id]))
        self.assertEqual(response.status_code, 200)

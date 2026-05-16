from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.biblioteca.models.biblioteca import Livro, Emprestimo
from apps.usuarios.models.perfis import Aluno, Professor
from apps.academico.models import Turma
from django.utils import timezone

User = get_user_model()


class BibliotecaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"

        # Gestor
        self.gestor_user = User.objects.create_superuser(
            username="gestor", password=self.password
        )

        # Aluno
        self.aluno_user = User.objects.create_user(
            username="aluno", password=self.password
        )
        self.turma = Turma.objects.create(nome="1A", turno="manha", ano=2024)
        self.aluno = Aluno.objects.create(
            user=self.aluno_user,
            nome_completo="Aluno 1",
            cpf="1",
            data_nascimento="2010-01-01",
            turma=self.turma,
        )

        # Livro
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro", autor="Machado de Assis", quantidade_total=5
        )

    def test_acervo_biblioteca(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("acervo_biblioteca"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dom Casmurro")

    def test_detalhe_livro(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("detalhe_livro", args=[self.livro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dom Casmurro")

    def test_reservar_livro(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.post(reverse("reservar_livro", args=[self.livro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Emprestimo.objects.filter(
                livro=self.livro, usuario_aluno=self.aluno
            ).count(),
            1,
        )

    def test_gerenciar_emprestimos_gestor(self):
        self.client.login(username="gestor", password=self.password)
        response = self.client.get(reverse("gerenciar_emprestimos"))
        self.assertEqual(response.status_code, 200)

    def test_gerenciar_emprestimos_aluno_negado(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("gerenciar_emprestimos"))
        # user_passes_test redireciona para login ou mostra 403 dependendo da config, mas aqui deve ser redirecionado se não passar
        self.assertEqual(response.status_code, 302)

    def test_novo_emprestimo(self):
        self.client.login(username="gestor", password=self.password)
        # Simplificando o form data
        data = {
            "livro": self.livro.id,
            "usuario_aluno": self.aluno.id,
            "data_devolucao_prevista": (
                timezone.now() + timezone.timedelta(days=14)
            ).date(),
            "status": "ATIVO",
        }
        response = self.client.post(reverse("novo_emprestimo"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Emprestimo.objects.filter(status="ATIVO").count(), 1)

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Professor
from apps.academico.models.academico import Turma, Disciplina, AtividadeProfessor

User = get_user_model()


class AcademicoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"

        # Superusuário para cadastros
        self.super_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password=self.password
        )

        # Professor
        self.prof_user = User.objects.create_user(
            username="prof", email="prof@test.com", password=self.password
        )
        self.professor = Professor.objects.create(
            user=self.prof_user,
            nome_completo="Prof Teste",
            cpf="111.111.111-11",
            data_nascimento="1980-01-01",
        )

        # Turma e Disciplina
        self.turma = Turma.objects.create(
            nome="1A", turno="manha", ano=timezone.now().year
        )
        self.disciplina = Disciplina.objects.create(
            nome="Matemática", professor=self.professor, turma=self.turma
        )

        # Aluno
        self.aluno_user = User.objects.create_user(
            username="aluno", email="aluno@test.com", password=self.password
        )
        self.aluno = Aluno.objects.create(
            user=self.aluno_user,
            nome_completo="Aluno Teste",
            cpf="222.222.222-22",
            data_nascimento="2010-01-01",
            turma=self.turma,
        )

    def test_visualizar_disciplinas_acesso_professor(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(
            reverse("visualizar_disciplinas", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["disciplina"], self.disciplina)

    def test_listar_turmas_acesso_admin(self):
        self.client.login(username="admin", password=self.password)
        response = self.client.get(reverse("listar_turmas"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.turma, response.context["turmas"])

    def test_listar_atividades_acesso_professor(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(
            reverse("listar_atividades", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_atividade_get(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(
            reverse("cadastrar_atividade", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_listar_atividades_aluno(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("listar_atividades_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_listar_materiais_aluno(self):
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("listar_materiais_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_disciplina_post(self):
        self.client.login(username="admin", password=self.password)
        data = {
            "nome": "Física",
            "professor": self.professor.id,
            "turma": self.turma.id,
        }
        response = self.client.post(
            reverse("cadastrar_disciplina_para_turma", args=[self.turma.id]), data
        )
        self.assertTrue(Disciplina.objects.filter(nome="Física").exists())
        self.assertRedirects(
            response, reverse("listar_disciplinas_turma", args=[self.turma.id])
        )

    def test_cadastrar_atividade_post(self):
        self.client.login(username="prof", password=self.password)
        data = {
            "titulo": "Novo Trabalho",
            "tipo": "TRABALHO",
            "data": "2024-05-10",
            "prazo_final": "2024-05-20T23:59",
            "valor": "10.0",
        }
        response = self.client.post(
            reverse("cadastrar_atividade", args=[self.disciplina.id]), data
        )
        self.assertTrue(
            AtividadeProfessor.objects.filter(titulo="Novo Trabalho").exists()
        )
        self.assertRedirects(
            response, reverse("listar_atividades", args=[self.disciplina.id])
        )

    def test_cadastrar_turma_post(self):
        self.client.login(username="admin", password=self.password)
        data = {"nome": "2B", "turno": "tarde", "ano": 2024}
        response = self.client.post(reverse("cadastrar_turma"), data)
        self.assertTrue(Turma.objects.filter(nome="2B").exists())
        self.assertRedirects(response, reverse("listar_turmas"))

    def test_editar_turma_post(self):
        self.client.login(username="admin", password=self.password)
        data = {"nome": "1A-Editada", "turno": "noite", "ano": 2024}
        response = self.client.post(reverse("editar_turma", args=[self.turma.id]), data)
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, "1A-Editada")
        self.assertRedirects(response, reverse("listar_turmas"))

    def test_grade_horaria_get(self):
        self.client.login(username="admin", password=self.password)
        response = self.client.get(reverse("grade_horaria", args=[self.turma.id]))
        self.assertEqual(response.status_code, 200)

    def test_lancar_notas_atividade_post(self):
        self.client.login(username="prof", password=self.password)
        atividade = AtividadeProfessor.objects.create(
            titulo="Atividade com Nota",
            tipo="ATIVIDADE",
            data="2024-05-10",
            prazo_final=timezone.now(),
            disciplina=self.disciplina,
        )
        data = {f"nota_{self.aluno.id}": "8.5", f"obs_{self.aluno.id}": "Bom trabalho"}
        response = self.client.post(
            reverse("lancar_notas_atividade", args=[self.disciplina.id, atividade.id]),
            data,
        )
        self.assertEqual(response.status_code, 302)

        from apps.academico.models.desempenho import NotaAtividade

        self.assertTrue(
            NotaAtividade.objects.filter(
                aluno=self.aluno, atividade=atividade, valor=8.5
            ).exists()
        )

    def test_visualizar_grade_professor_get(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(
            reverse("visualizar_grade_professor", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_professor_get(self):
        self.client.login(username="prof", password=self.password)
        response = self.client.get(reverse("disciplinas_professor"))
        self.assertEqual(response.status_code, 200)

    def test_excluir_disciplina(self):
        self.client.login(username="admin", password=self.password)
        response = self.client.post(
            reverse("excluir_disciplina", args=[self.disciplina.id])
        )
        self.assertFalse(Disciplina.objects.filter(id=self.disciplina.id).exists())
        self.assertRedirects(
            response, reverse("listar_disciplinas_turma", args=[self.turma.id])
        )

    def test_excluir_turma(self):
        self.client.login(username="admin", password=self.password)
        response = self.client.post(reverse("excluir_turma", args=[self.turma.id]))
        self.assertFalse(Turma.objects.filter(id=self.turma.id).exists())
        self.assertRedirects(response, reverse("listar_turmas"))

    def test_marcar_notificacao_lida(self):
        from apps.academico.models.desempenho import Notificacao

        notif = Notificacao.objects.create(
            usuario=self.aluno_user, titulo="Teste", mensagem="Msg"
        )
        self.client.login(username="aluno", password=self.password)
        response = self.client.get(reverse("marcar_notificacao_lida", args=[notif.id]))
        notif.refresh_from_db()
        self.assertTrue(notif.lida)
        self.assertEqual(response.status_code, 302)

    def test_marcar_todas_notificacoes_lidas(self):
        from apps.academico.models.desempenho import Notificacao

        Notificacao.objects.create(usuario=self.aluno_user, titulo="T1", mensagem="M1")
        Notificacao.objects.create(usuario=self.aluno_user, titulo="T2", mensagem="M2")
        self.client.login(username="aluno", password=self.password)
        self.client.get(reverse("marcar_todas_notificacoes_lidas"))
        self.assertFalse(
            Notificacao.objects.filter(usuario=self.aluno_user, lida=False).exists()
        )

    def test_controlar_liberacao_gabarito_sim(self):
        atividade = AtividadeProfessor.objects.create(
            titulo="Ativ Gabarito",
            tipo="ATIVIDADE",
            data="2024-05-10",
            prazo_final=timezone.now(),
            disciplina=self.disciplina,
        )
        # Adiciona uma questão para poder liberar gabarito
        from apps.academico.models.academico import Questao

        Questao.objects.create(
            atividade=atividade, enunciado="Q1", tipo="MULTIPLA_ESCOLHA"
        )

        self.client.login(username="prof", password=self.password)
        response = self.client.post(
            reverse(
                "controlar_liberacao_gabarito", args=[self.disciplina.id, atividade.id]
            ),
            {"decisao": "sim"},
        )
        atividade.refresh_from_db()
        self.assertTrue(atividade.gabarito_liberado)

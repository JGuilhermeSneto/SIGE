"""
Testes para apps.academico.models.desempenho_v8.

Cobre:
- Nota.media (com diversas combinações de notas)
- Nota.__str__
- Notificacao.__str__
- RiscoEvasao.__str__
- Signal alerta_risco_critico (dispara ou não dependendo do score)
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.academico.models import Disciplina, Turma
from apps.academico.models.desempenho_v8 import (
    Nota,
    Notificacao,
    RiscoEvasao,
)
from apps.usuarios.models.perfis import Aluno, Professor

User = get_user_model()


def _make_user(username):
    return User.objects.create_user(username=username, password="pass")


class BaseDesempenhoTestCase(TestCase):
    """Cria objetos base reutilizados nos testes de desempenho."""

    def setUp(self):
        prof_user = _make_user("prof_desemp")
        self.professor = Professor.objects.create(
            user=prof_user,
            nome_completo="Prof Desempenho",
            cpf="010.020.030-40",
            data_nascimento="1978-03-12",
        )
        self.turma = Turma.objects.create(nome="4A", turno="manha", ano=2024)
        aluno_user = _make_user("aluno_desemp")
        self.aluno = Aluno.objects.create(
            user=aluno_user,
            nome_completo="Aluno Desempenho",
            cpf="050.060.070-80",
            data_nascimento="2009-11-25",
            turma=self.turma,
        )
        self.disciplina = Disciplina.objects.create(
            nome="História",
            professor=self.professor,
            turma=self.turma,
        )


class NotaMediaTest(BaseDesempenhoTestCase):
    """Testa a propriedade `media` do model Nota."""

    def _criar_nota(self, **notas):
        return Nota.objects.create(
            aluno=self.aluno, disciplina=self.disciplina, **notas
        )

    def test_media_com_quatro_notas(self):
        nota = self._criar_nota(nota1=8, nota2=7, nota3=9, nota4=6)
        self.assertAlmostEqual(float(nota.media), 7.5, places=5)

    def test_media_com_uma_nota(self):
        nota = self._criar_nota(nota1=10)
        self.assertAlmostEqual(float(nota.media), 10.0, places=5)

    def test_media_com_notas_parciais(self):
        nota = self._criar_nota(nota1=6, nota2=8)
        self.assertAlmostEqual(float(nota.media), 7.0, places=5)

    def test_media_sem_notas_retorna_none(self):
        nota = self._criar_nota()
        self.assertIsNone(nota.media)

    def test_media_com_nota_zero(self):
        nota = self._criar_nota(nota1=0, nota2=0, nota3=0, nota4=0)
        self.assertAlmostEqual(float(nota.media), 0.0, places=5)


class NotaStrTest(BaseDesempenhoTestCase):
    """Testa o método __str__ do model Nota."""

    def test_str_com_notas(self):
        nota = Nota.objects.create(
            aluno=self.aluno, disciplina=self.disciplina, nota1=7, nota2=8
        )
        resultado = str(nota)
        self.assertIn("Aluno Desempenho", resultado)
        self.assertIn("História", resultado)
        self.assertIn("7.50", resultado)

    def test_str_sem_notas_exibe_na(self):
        nota = Nota.objects.create(aluno=self.aluno, disciplina=self.disciplina)
        resultado = str(nota)
        self.assertIn("N/A", resultado)


class NotificacaoStrTest(TestCase):
    """Testa o método __str__ do model Notificacao."""

    def test_str_exibe_username_e_titulo(self):
        user = _make_user("user_notif_str")
        notif = Notificacao.objects.create(
            usuario=user,
            tipo="SISTEMA",
            titulo="Aviso importante",
            mensagem="Detalhes do aviso.",
        )
        resultado = str(notif)
        self.assertIn("user_notif_str", resultado)
        self.assertIn("Aviso importante", resultado)


class RiscoEvasaoTest(BaseDesempenhoTestCase):
    """Testa RiscoEvasao e o signal alerta_risco_critico."""

    def test_str_exibe_aluno_e_score(self):
        risco = RiscoEvasao.objects.create(
            aluno=self.aluno, score=45.0, fatores="Baixa frequência"
        )
        resultado = str(risco)
        self.assertIn("45", resultado)

    def test_signal_nao_dispara_para_score_abaixo_de_80(self):
        """Score < 80 não deve criar notificações."""
        # Superusuário para receber alertas
        User.objects.create_superuser("admin_risco", password="admin")
        Notificacao.objects.all().delete()

        RiscoEvasao.objects.create(aluno=self.aluno, score=79.99, fatores="Leve")

        self.assertEqual(Notificacao.objects.count(), 0)

    def test_signal_dispara_para_score_igual_a_80(self):
        """Score == 80 deve criar notificação para cada superusuário."""
        su = User.objects.create_superuser("admin_alerta80", password="admin")
        Notificacao.objects.all().delete()

        RiscoEvasao.objects.create(aluno=self.aluno, score=80, fatores="Frequência")

        notifs = Notificacao.objects.filter(usuario=su)
        self.assertEqual(notifs.count(), 1)
        self.assertEqual(notifs.first().tipo, "SISTEMA")
        self.assertIn("ALERTA CRÍTICO", notifs.first().titulo)

    def test_signal_dispara_para_score_acima_de_80(self):
        """Score > 80 deve criar notificação."""
        su = User.objects.create_superuser("admin_alerta95", password="admin")
        Notificacao.objects.all().delete()

        RiscoEvasao.objects.create(
            aluno=self.aluno, score=95.5, fatores="Alta evasão"
        )

        notifs = Notificacao.objects.filter(usuario=su)
        self.assertEqual(notifs.count(), 1)
        self.assertIn("95.5", notifs.first().mensagem)

    def test_signal_notifica_multiplos_superusuarios(self):
        """Todos os superusuários devem ser notificados."""
        su1 = User.objects.create_superuser("admin_multi1", password="admin")
        su2 = User.objects.create_superuser("admin_multi2", password="admin")
        Notificacao.objects.all().delete()

        RiscoEvasao.objects.create(aluno=self.aluno, score=90, fatores="Múltiplos")

        ids = set(Notificacao.objects.values_list("usuario_id", flat=True))
        self.assertIn(su1.id, ids)
        self.assertIn(su2.id, ids)

    def test_signal_nao_dispara_no_update_com_score_critico(self):
        """O signal dispara em cada save; update de um risco já existente deve criar nova notificação."""
        su = User.objects.create_superuser("admin_update", password="admin")
        Notificacao.objects.all().delete()

        risco = RiscoEvasao.objects.create(aluno=self.aluno, score=85, fatores="Critico")
        count_apos_criacao = Notificacao.objects.filter(usuario=su).count()
        self.assertEqual(count_apos_criacao, 1)

        # Re-salvar (update) também deve disparar o signal
        risco.fatores = "Frequência muito baixa"
        risco.save()
        self.assertEqual(Notificacao.objects.filter(usuario=su).count(), 2)

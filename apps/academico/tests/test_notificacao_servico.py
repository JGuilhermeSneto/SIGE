"""
Testes para apps.academico.services.notificacao_servico.

Cobre os métodos: criar, criar_para_turma, notificar_gestores,
notificar_todos e notificar_grupo.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.academico.models import Notificacao, Turma
from apps.academico.services.notificacao_servico import NotificacaoServico
from apps.usuarios.models.perfis import Aluno, Gestor, Professor

User = get_user_model()


def _make_user(username, **kwargs):
    return User.objects.create_user(username=username, password="pass", **kwargs)


class NotificacaoServicoCriarTest(TestCase):
    """Testa o método estático `criar` (e seu alias `notificar_usuario`)."""

    def setUp(self):
        self.user = _make_user("destino1")

    def test_criar_grava_notificacao_no_banco(self):
        notif = NotificacaoServico.criar(
            user=self.user,
            tipo="SISTEMA",
            titulo="Título teste",
            mensagem="Mensagem de teste",
            url_destino="/alguma/url/",
        )
        self.assertEqual(Notificacao.objects.count(), 1)
        self.assertEqual(notif.usuario, self.user)
        self.assertEqual(notif.tipo, "SISTEMA")
        self.assertEqual(notif.titulo, "Título teste")
        self.assertEqual(notif.url_destino, "/alguma/url/")
        self.assertFalse(notif.lida)

    def test_criar_sem_url_destino_usa_string_vazia(self):
        notif = NotificacaoServico.criar(
            user=self.user,
            tipo="MENSAGEM",
            titulo="Sem URL",
            mensagem="Mensagem.",
        )
        self.assertEqual(notif.url_destino, "")

    def test_criar_com_url_destino_none_usa_string_vazia(self):
        notif = NotificacaoServico.criar(
            user=self.user,
            tipo="MENSAGEM",
            titulo="URL None",
            mensagem="Mensagem.",
            url_destino=None,
        )
        self.assertEqual(notif.url_destino, "")

    def test_alias_notificar_usuario_e_identico_a_criar(self):
        # O alias deve ser o mesmo callable que criar
        self.assertIs(NotificacaoServico.notificar_usuario, NotificacaoServico.criar)


class NotificacaoServicoCriarParaTurmaTest(TestCase):
    """Testa `criar_para_turma`."""

    def setUp(self):
        self.turma = Turma.objects.create(nome="3B", turno="tarde", ano=2024)

        self.professor_user = _make_user("prof_notif")
        self.professor = Professor.objects.create(
            user=self.professor_user,
            nome_completo="Prof Notif",
            cpf="000.111.222-33",
            data_nascimento="1975-06-10",
        )

    def _criar_aluno(self, username, cpf):
        u = _make_user(username)
        return Aluno.objects.create(
            user=u,
            nome_completo=f"Aluno {username}",
            cpf=cpf,
            data_nascimento="2010-03-15",
            turma=self.turma,
        )

    def test_notifica_todos_alunos_da_turma(self):
        aluno1 = self._criar_aluno("aluno_a", "100.200.300-01")
        aluno2 = self._criar_aluno("aluno_b", "100.200.300-02")

        NotificacaoServico.criar_para_turma(
            turma=self.turma,
            tipo="NOTA",
            titulo="Nova nota",
            mensagem="Nota lançada pelo professor.",
            url_destino="/notas/",
        )

        notifs = Notificacao.objects.all()
        self.assertEqual(notifs.count(), 2)
        destinatarios = set(notifs.values_list("usuario_id", flat=True))
        self.assertIn(aluno1.user_id, destinatarios)
        self.assertIn(aluno2.user_id, destinatarios)

    def test_turma_sem_alunos_nao_cria_notificacoes(self):
        NotificacaoServico.criar_para_turma(
            turma=self.turma,
            tipo="NOTA",
            titulo="Nota",
            mensagem="Vazia",
        )
        self.assertEqual(Notificacao.objects.count(), 0)

    def test_url_destino_nao_informada_usa_vazio(self):
        self._criar_aluno("aluno_c", "111.222.333-44")
        NotificacaoServico.criar_para_turma(
            turma=self.turma,
            tipo="SISTEMA",
            titulo="Aviso",
            mensagem="Mensagem sem URL.",
        )
        notif = Notificacao.objects.first()
        self.assertEqual(notif.url_destino, "")


class NotificacaoServicoNotificarGestoresTest(TestCase):
    """Testa `notificar_gestores`."""

    def test_notifica_gestor_cadastrado(self):
        gestor_user = _make_user("gestor1")
        Gestor.objects.create(
            user=gestor_user,
            nome_completo="Gestor Um",
            cpf="555.666.777-88",
            data_nascimento="1970-01-01",
            cargo="diretor",
        )

        NotificacaoServico.notificar_gestores(
            tipo="ATESTADO",
            titulo="Novo atestado",
            mensagem="Um atestado foi enviado.",
            url_destino="/saude/atestados/",
        )

        notifs = Notificacao.objects.filter(usuario=gestor_user)
        self.assertEqual(notifs.count(), 1)
        self.assertEqual(notifs.first().tipo, "ATESTADO")

    def test_notifica_superusuario(self):
        su = User.objects.create_superuser("superadmin", password="admin123")

        NotificacaoServico.notificar_gestores(
            tipo="SISTEMA",
            titulo="Alerta sistema",
            mensagem="Problema crítico.",
        )

        self.assertEqual(Notificacao.objects.filter(usuario=su).count(), 1)

    def test_sem_gestores_nao_cria_notificacoes(self):
        # Nenhum superuser nem gestor existente
        NotificacaoServico.notificar_gestores(
            tipo="SISTEMA",
            titulo="Sem gestores",
            mensagem="Nada.",
        )
        self.assertEqual(Notificacao.objects.count(), 0)


class NotificacaoServicoNotificarTodosTest(TestCase):
    """Testa `notificar_todos`."""

    def test_notifica_todos_usuarios_ativos(self):
        u1 = _make_user("user_ativo1")
        u2 = _make_user("user_ativo2")
        u_inativo = _make_user("user_inativo")
        u_inativo.is_active = False
        u_inativo.save()

        NotificacaoServico.notificar_todos(
            tipo="SISTEMA",
            titulo="Aviso geral",
            mensagem="Comunicado para todos.",
        )

        # Só ativos devem receber
        ids_notificados = set(Notificacao.objects.values_list("usuario_id", flat=True))
        self.assertIn(u1.id, ids_notificados)
        self.assertIn(u2.id, ids_notificados)
        self.assertNotIn(u_inativo.id, ids_notificados)

    def test_campos_da_notificacao_corretos(self):
        u = _make_user("user_campos")
        NotificacaoServico.notificar_todos(
            tipo="MENSAGEM",
            titulo="Título global",
            mensagem="Corpo da mensagem.",
            url_destino="/inicio/",
        )
        notif = Notificacao.objects.get(usuario=u)
        self.assertEqual(notif.titulo, "Título global")
        self.assertEqual(notif.url_destino, "/inicio/")


class NotificacaoServicoNotificarGrupoTest(TestCase):
    """Testa `notificar_grupo`."""

    def test_notifica_apenas_usuarios_do_queryset(self):
        u1 = _make_user("grupo_u1")
        u2 = _make_user("grupo_u2")
        u3 = _make_user("grupo_u3")

        grupo = User.objects.filter(id__in=[u1.id, u2.id])

        NotificacaoServico.notificar_grupo(
            usuarios_queryset=grupo,
            tipo="MENSAGEM",
            titulo="Mensagem do grupo",
            mensagem="Somente vocês.",
            url_destino="/grupo/",
        )

        ids_notificados = set(Notificacao.objects.values_list("usuario_id", flat=True))
        self.assertIn(u1.id, ids_notificados)
        self.assertIn(u2.id, ids_notificados)
        self.assertNotIn(u3.id, ids_notificados)

    def test_queryset_vazio_nao_cria_notificacoes(self):
        NotificacaoServico.notificar_grupo(
            usuarios_queryset=User.objects.none(),
            tipo="SISTEMA",
            titulo="Vazio",
            mensagem="Ninguém.",
        )
        self.assertEqual(Notificacao.objects.count(), 0)

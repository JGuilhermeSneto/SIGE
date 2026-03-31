"""
Testes para core/views.py - SIGE
Cobertura alvo: 32% → 75%+

Execute com:
    coverage run manage.py test core.test.test_views_completo
    coverage report
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import (
    Aluno,
    Disciplina,
    Gestor,
    GradeHorario,
    Nota,
    Professor,
    Turma,
)

User = get_user_model()


# ================================================================
# FACTORIES — criam objetos reutilizáveis nos testes
# ================================================================

def criar_superuser(username="admin", password="123456"):
    return User.objects.create_superuser(
        username=username, password=password, email=f"{username}@test.com"
    )


def criar_user_comum(username="user", password="123456"):
    return User.objects.create_user(
        username=username, password=password, email=f"{username}@test.com"
    )


def criar_professor(username="prof", password="123456", nome="Professor Teste"):
    user = User.objects.create_user(
        username=username, password=password, email=f"{username}@test.com"
    )
    professor = Professor.objects.create(user=user, nome_completo=nome)
    return professor


def criar_gestor(username="gestor", password="123456", nome="Gestor Teste", cargo="diretor"):
    user = User.objects.create_user(
        username=username, password=password, email=f"{username}@test.com"
    )
    gestor = Gestor.objects.create(user=user, nome_completo=nome, cargo=cargo)
    return gestor


def criar_turma(nome="9A", turno="manha", ano=2024):
    return Turma.objects.create(nome=nome, turno=turno, ano=ano)


def criar_aluno(turma, username="aluno", password="123456", nome="Aluno Teste"):
    user = User.objects.create_user(
        username=username, password=password, email=f"{username}@test.com"
    )
    aluno = Aluno.objects.create(user=user, nome_completo=nome, turma=turma)
    return aluno


def criar_disciplina(turma, professor, nome="Matemática"):
    return Disciplina.objects.create(nome=nome, turma=turma, professor=professor)


# ================================================================
# LOGIN / LOGOUT
# ================================================================

class LoginViewTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        turma = criar_turma()
        self.aluno = criar_aluno(turma)

    def test_login_get_retorna_200(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_usuario_ja_autenticado_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)

    def test_login_post_credenciais_invalidas(self):
        response = self.client.post(reverse("login"), {
            "username": "naoexiste",
            "password": "errada"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_post_superuser_redireciona_para_painel_super(self):
        response = self.client.post(reverse("login"), {
            "username": "admin",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_professor_redireciona_para_painel_professor(self):
        response = self.client.post(reverse("login"), {
            "username": "prof",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_aluno_redireciona_para_painel_aluno(self):
        response = self.client.post(reverse("login"), {
            "username": "aluno",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_redireciona_para_login(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))


# ================================================================
# PAINEL SUPER
# ================================================================

class PainelSuperTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.gestor = criar_gestor()
        self.user_comum = criar_user_comum()

    def test_sem_login_redireciona(self):
        response = self.client.get(reverse("painel_super"))
        self.assertEqual(response.status_code, 302)

    def test_user_comum_sem_permissao(self):
        self.client.force_login(self.user_comum)
        response = self.client.get(reverse("painel_super"))
        self.assertEqual(response.status_code, 302)

    def test_superuser_acessa_painel(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("painel_super"))
        self.assertEqual(response.status_code, 200)

    def test_gestor_acessa_painel(self):
        self.client.force_login(self.gestor.user)
        response = self.client.get(reverse("painel_super"))
        self.assertEqual(response.status_code, 200)

    def test_filtro_por_ano(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("painel_super") + "?ano=2023")
        self.assertEqual(response.status_code, 200)

    def test_filtro_ano_invalido_usa_ano_atual(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("painel_super") + "?ano=abc")
        self.assertEqual(response.status_code, 200)


# ================================================================
# PERFIL
# ================================================================

class EditarPerfilTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        turma = criar_turma()
        self.aluno = criar_aluno(turma)

    def test_get_retorna_200(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("editar_perfil"))
        self.assertEqual(response.status_code, 200)

    def test_post_valido_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("editar_perfil"), {
            "username": "admin",
            "email": "admin@test.com",
            "first_name": "Admin",
            "last_name": "Teste",
        })
        self.assertEqual(response.status_code, 302)

    def test_post_invalido_mostra_erro(self):
        self.client.force_login(self.superuser)
        # email inválido deve falhar na validação
        response = self.client.post(reverse("editar_perfil"), {
            "email": "email-invalido",
        })
        self.assertEqual(response.status_code, 200)

    def test_perfil_professor_tem_foto_atual(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(reverse("editar_perfil"))
        self.assertEqual(response.status_code, 200)

    def test_perfil_aluno_tem_foto_atual(self):
        self.client.force_login(self.aluno.user)
        response = self.client.get(reverse("editar_perfil"))
        self.assertEqual(response.status_code, 200)


class RemoverFotoPerfilTest(TestCase):

    def setUp(self):
        self.user_sem_perfil = criar_user_comum()
        self.superuser = criar_superuser()

    def test_usuario_sem_perfil_mostra_erro(self):
        self.client.force_login(self.user_sem_perfil)
        response = self.client.get(reverse("remover_foto_perfil"))
        self.assertRedirects(response, reverse("editar_perfil"))

    def test_superuser_sem_foto_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("remover_foto_perfil"))
        # superuser não tem perfil com foto, deve redirecionar
        self.assertEqual(response.status_code, 302)


# ================================================================
# PROFESSORES
# ================================================================

class ProfessorViewsTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.gestor = criar_gestor()
        self.professor = criar_professor()
        self.user_comum = criar_user_comum()

    def test_listar_sem_permissao_redireciona(self):
        self.client.force_login(self.user_comum)
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 302)

    def test_listar_com_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_com_gestor(self):
        self.client.force_login(self.gestor.user)
        response = self.client.get(reverse("listar_professores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_com_busca(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_professores") + "?q=Professor")
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("cadastrar_professor"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_professor"), {})
        self.assertEqual(response.status_code, 200)

    def test_editar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("editar_professor", args=[self.professor.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("editar_professor", args=[self.professor.id]), {}
        )
        self.assertEqual(response.status_code, 200)

    def test_excluir_professor(self):
        prof_extra = criar_professor(username="prof2", nome="Extra")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("excluir_professor", args=[prof_extra.id])
        )
        self.assertRedirects(response, reverse("listar_professores"))
        self.assertFalse(Professor.objects.filter(id=prof_extra.id).exists())


# ================================================================
# GESTORES
# ================================================================

class GestorViewsTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.gestor = criar_gestor()
        self.user_comum = criar_user_comum()

    def test_listar_gestores_com_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_gestores"))
        self.assertEqual(response.status_code, 200)

    def test_listar_gestores_sem_superuser_redireciona(self):
        self.client.force_login(self.user_comum)
        response = self.client.get(reverse("listar_gestores"))
        self.assertEqual(response.status_code, 302)

    def test_cadastrar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("cadastrar_gestor"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_gestor"), {})
        self.assertEqual(response.status_code, 200)

    def test_editar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("editar_gestor", args=[self.gestor.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("editar_gestor", args=[self.gestor.id]), {}
        )
        self.assertEqual(response.status_code, 200)

    def test_excluir_gestor(self):
        gestor_extra = criar_gestor(username="gestor2", nome="Gestor Extra")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("excluir_gestor", args=[gestor_extra.id])
        )
        self.assertRedirects(response, reverse("listar_gestores"))
        self.assertFalse(Gestor.objects.filter(id=gestor_extra.id).exists())


# ================================================================
# ALUNOS
# ================================================================

class AlunoViewsTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.turma = criar_turma()
        self.aluno = criar_aluno(self.turma)

    def test_listar_sem_login_redireciona(self):
        response = self.client.get(reverse("listar_alunos"))
        self.assertEqual(response.status_code, 302)

    def test_listar_com_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_alunos"))
        self.assertEqual(response.status_code, 200)

    def test_listar_com_busca(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_alunos") + "?q=Aluno")
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("cadastrar_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_aluno"), {})
        self.assertEqual(response.status_code, 200)

    def test_editar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("editar_aluno", args=[self.aluno.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_post_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("editar_aluno", args=[self.aluno.id]), {}
        )
        self.assertEqual(response.status_code, 200)

    def test_excluir_aluno(self):
        aluno_extra = criar_aluno(self.turma, username="aluno2", nome="Extra")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("excluir_aluno", args=[aluno_extra.id])
        )
        self.assertRedirects(response, reverse("listar_alunos"))
        self.assertFalse(Aluno.objects.filter(id=aluno_extra.id).exists())


# ================================================================
# TURMAS
# ================================================================

class TurmaViewsTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.turma = criar_turma()

    def test_listar_com_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_turmas"))
        self.assertEqual(response.status_code, 200)

    def test_listar_com_filtro_ano(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_turmas") + "?ano=2024")
        self.assertEqual(response.status_code, 200)

    def test_listar_com_busca(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("listar_turmas") + "?q=9A")
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("cadastrar_turma"))
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_post_valido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_turma"), {
            "nome": "8B",
            "turno": "tarde",
            "ano": "2024",
        })
        self.assertRedirects(response, reverse("listar_turmas"))
        self.assertTrue(Turma.objects.filter(nome="8B").exists())

    def test_cadastrar_post_turma_duplicada(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_turma"), {
            "nome": "9A",
            "turno": "manha",
            "ano": "2024",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "já existe")

    def test_cadastrar_post_ano_invalido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_turma"), {
            "nome": "7C",
            "turno": "manha",
            "ano": "abc",
        })
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_post_ano_fora_do_intervalo(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("cadastrar_turma"), {
            "nome": "7C",
            "turno": "manha",
            "ano": "1990",
        })
        self.assertEqual(response.status_code, 200)

    def test_editar_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("editar_turma", args=[self.turma.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_post_valido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("editar_turma", args=[self.turma.id]), {
            "nome": "9A Atualizado",
            "turno": "tarde",
            "ano": "2024",
        })
        self.assertRedirects(response, reverse("listar_turmas"))

    def test_editar_post_nome_duplicado(self):
        outra = criar_turma(nome="9B")
        self.client.force_login(self.superuser)
        # tenta renomear self.turma para o mesmo nome de outra
        response = self.client.post(reverse("editar_turma", args=[self.turma.id]), {
            "nome": "9B",
            "turno": "manha",
            "ano": str(outra.ano),
        })
        self.assertEqual(response.status_code, 200)

    def test_excluir_turma(self):
        turma_extra = criar_turma(nome="7A")
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("excluir_turma", args=[turma_extra.id]))
        self.assertRedirects(response, reverse("listar_turmas"))
        self.assertFalse(Turma.objects.filter(id=turma_extra.id).exists())


# ================================================================
# DISCIPLINAS
# ================================================================

class DisciplinaViewsTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        self.turma = criar_turma()
        self.disciplina = criar_disciplina(self.turma, self.professor)

    def test_listar_disciplinas_turma(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("listar_disciplinas_turma", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_listar_disciplinas_turma_com_busca(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("listar_disciplinas_turma", args=[self.turma.id]) + "?q=Mate"
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_disciplina_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("cadastrar_disciplina_para_turma", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_disciplina_post_valido(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("cadastrar_disciplina_para_turma", args=[self.turma.id]),
            {"nome": "Português", "professor": self.professor.id},
        )
        self.assertRedirects(
            response, reverse("disciplinas_turma", args=[self.turma.id])
        )

    def test_cadastrar_disciplina_post_campos_vazios(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("cadastrar_disciplina_para_turma", args=[self.turma.id]),
            {"nome": "", "professor": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_disciplina_duplicada(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("cadastrar_disciplina_para_turma", args=[self.turma.id]),
            {"nome": "Matemática", "professor": self.professor.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_disciplina_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("editar_disciplina", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editar_disciplina_post(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("editar_disciplina", args=[self.disciplina.id]),
            {"nome": "Matemática Avançada", "professor": self.professor.id},
        )
        self.assertRedirects(
            response, reverse("disciplinas_turma", args=[self.turma.id])
        )

    def test_excluir_disciplina(self):
        disc_extra = criar_disciplina(self.turma, self.professor, nome="Física")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("excluir_disciplina", args=[disc_extra.id])
        )
        self.assertRedirects(
            response, reverse("disciplinas_turma", args=[self.turma.id])
        )
        self.assertFalse(Disciplina.objects.filter(id=disc_extra.id).exists())

    def test_visualizar_disciplina_como_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("visualizar_disciplinas", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_visualizar_disciplina_como_professor_da_disciplina(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(
            reverse("visualizar_disciplinas", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_visualizar_disciplina_sem_permissao(self):
        outro_prof = criar_professor(username="outroprof", nome="Outro")
        self.client.force_login(outro_prof.user)
        response = self.client.get(
            reverse("visualizar_disciplinas", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_disciplinas_turma_como_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("disciplinas_turma", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_turma_como_professor(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(
            reverse("disciplinas_turma", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_turma_sem_disciplinas_redireciona(self):
        turma_vazia = criar_turma(nome="5A")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("disciplinas_turma", args=[turma_vazia.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_disciplinas_turma_sem_permissao_redireciona(self):
        user_sem_perfil = criar_user_comum(username="semPerfil")
        self.client.force_login(user_sem_perfil)
        response = self.client.get(
            reverse("disciplinas_turma", args=[self.turma.id])
        )
        self.assertRedirects(response, reverse("login"))


# ================================================================
# PAINEL PROFESSOR
# ================================================================

class PainelProfessorTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        self.turma = criar_turma()
        self.disciplina = criar_disciplina(self.turma, self.professor)

    def test_sem_perfil_professor_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("painel_professor"))
        self.assertRedirects(response, reverse("login"))

    def test_com_perfil_professor_retorna_200(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(reverse("painel_professor"))
        self.assertEqual(response.status_code, 200)

    def test_filtro_por_ano(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(reverse("painel_professor") + "?ano=2024")
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_professor_retorna_200(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(reverse("disciplinas_professor"))
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_professor_com_busca(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(reverse("disciplinas_professor") + "?q=9A")
        self.assertEqual(response.status_code, 200)

    def test_disciplinas_professor_sem_perfil_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("disciplinas_professor"))
        self.assertRedirects(response, reverse("login"))

    def test_visualizar_grade_professor(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(
            reverse("visualizar_grade_professor", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_visualizar_grade_sem_disciplina_redireciona(self):
        turma_sem_disc = criar_turma(nome="6B")
        self.client.force_login(self.professor.user)
        response = self.client.get(
            reverse("visualizar_grade_professor", args=[turma_sem_disc.id])
        )
        self.assertRedirects(response, reverse("disciplinas_professor"))

    def test_visualizar_grade_sem_perfil_professor_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("visualizar_grade_professor", args=[self.turma.id])
        )
        self.assertRedirects(response, reverse("login"))


# ================================================================
# LANÇAR NOTAS
# ================================================================

class LancarNotaTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        self.turma = criar_turma()
        self.disciplina = criar_disciplina(self.turma, self.professor)
        self.aluno = criar_aluno(self.turma)

    def test_get_retorna_200_como_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("lancar_nota", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_get_retorna_200_como_professor(self):
        self.client.force_login(self.professor.user)
        response = self.client.get(
            reverse("lancar_nota", args=[self.disciplina.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_post_notas_validas(self):
        self.client.force_login(self.professor.user)
        response = self.client.post(
            reverse("lancar_nota", args=[self.disciplina.id]),
            {
                f"nota1_{self.aluno.pk}": "7.5",
                f"nota2_{self.aluno.pk}": "8.0",
                f"nota3_{self.aluno.pk}": "",
                f"nota4_{self.aluno.pk}": "",
            },
        )
        self.assertRedirects(
            response, reverse("lancar_nota", args=[self.disciplina.id])
        )
        nota = Nota.objects.get(aluno=self.aluno, disciplina=self.disciplina)
        self.assertEqual(nota.nota1, 7.5)
        self.assertEqual(nota.nota2, 8.0)

    def test_post_nota_invalida_mostra_erro(self):
        self.client.force_login(self.professor.user)
        response = self.client.post(
            reverse("lancar_nota", args=[self.disciplina.id]),
            {f"nota1_{self.aluno.pk}": "abc"},
        )
        # redireciona mesmo com erro (salva o que pode e exibe mensagem)
        self.assertEqual(response.status_code, 302)

    def test_post_nota_com_virgula(self):
        """Garante que notas com vírgula (ex: '7,5') são aceitas."""
        self.client.force_login(self.professor.user)
        self.client.post(
            reverse("lancar_nota", args=[self.disciplina.id]),
            {f"nota1_{self.aluno.pk}": "7,5"},
        )
        nota = Nota.objects.get(aluno=self.aluno, disciplina=self.disciplina)
        self.assertEqual(nota.nota1, 7.5)


# ================================================================
# PAINEL ALUNO
# ================================================================

class PainelAlunoTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        self.turma = criar_turma()
        self.aluno = criar_aluno(self.turma)
        self.disciplina = criar_disciplina(self.turma, self.professor)

    def test_sem_perfil_aluno_redireciona(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("painel_aluno"))
        self.assertRedirects(response, reverse("login"))

    def test_com_perfil_aluno_retorna_200(self):
        self.client.force_login(self.aluno.user)
        response = self.client.get(reverse("painel_aluno"))
        self.assertEqual(response.status_code, 200)

    def test_painel_aluno_com_notas_lancadas(self):
        Nota.objects.create(
            aluno=self.aluno,
            disciplina=self.disciplina,
            nota1=8.0,
            nota2=7.0,
            nota3=9.0,
            nota4=6.0,
        )
        self.client.force_login(self.aluno.user)
        response = self.client.get(reverse("painel_aluno"))
        self.assertEqual(response.status_code, 200)


# ================================================================
# GRADE HORÁRIA
# ================================================================

class GradeHorariaTest(TestCase):

    def setUp(self):
        self.superuser = criar_superuser()
        self.professor = criar_professor()
        self.turma = criar_turma()
        self.disciplina = criar_disciplina(self.turma, self.professor)

    def test_get_cria_grade_se_nao_existir(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("grade_horaria", args=[self.turma.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(GradeHorario.objects.filter(turma=self.turma).exists())

    def test_post_salva_grade(self):
        self.client.force_login(self.superuser)
        data = {}
        dias = ["segunda", "terca", "quarta", "quinta", "sexta"]
        for dia in dias:
            for i in range(6):
                data[f"{dia}_{i}"] = "Matemática" if i == 0 else ""
        response = self.client.post(
            reverse("grade_horaria", args=[self.turma.id]), data
        )
        self.assertRedirects(
            response, reverse("grade_horaria", args=[self.turma.id])
        )

    def test_grade_com_turno_tarde(self):
        turma_tarde = criar_turma(nome="8A", turno="tarde")
        criar_disciplina(turma_tarde, self.professor, nome="Física")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("grade_horaria", args=[turma_tarde.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_grade_com_turno_noite(self):
        turma_noite = criar_turma(nome="8B", turno="noite")
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("grade_horaria", args=[turma_noite.id])
        )
        self.assertEqual(response.status_code, 200)
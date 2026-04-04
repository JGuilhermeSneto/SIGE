"""
Testes de cobertura máxima para as funções duplicadas corrigidas em views.py.

Duplicatas identificadas e resolvidas:
  1. is_super_ou_gestor     — duas versões; mantida a 2ª (checa is_active)
  2. get_foto_perfil        — duas versões; mantida a 2ª (try/except por tipo)
  3. get_nome_exibicao      — duas versões; mantida a 2ª (fallback por email)
  4. login_view             — duas versões; mantida a 2ª (código mais limpo)
  5. logout_view            — duas versões; mantida a 2ª (sem message desnecessária)
  6. _calcular_situacao_aluno — assinaturas DIFERENTES; 1ª renomeada para
                               _calcular_situacao_nota_freq, 2ª mantida como
                               _calcular_situacao_aluno (usada por painel_aluno)
  7. _contar_notas_lancadas — duas versões; mantida a 2ª (aggregate por bimestre)
"""

from datetime import date
from unittest.mock import MagicMock, PropertyMock, patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import RequestFactory, TestCase
from django.urls import reverse

User = get_user_model()


# ===========================================================================
# Helpers de mock reutilizáveis
# ===========================================================================

def _make_user(is_superuser=False, is_active=True, has_gestor=False,
               has_professor=False, has_aluno=False,
               first_name="", last_name="", email="u@test.com"):
    """Cria um mock de User com os atributos necessários."""
    user = MagicMock(spec=User)
    user.is_superuser = is_superuser
    user.is_active = is_active
    user.is_authenticated = True
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.username = "testuser"

    # Remove ou adiciona relacionamentos
    if not has_gestor:
        del user.gestor
        user.__bool__ = lambda s: True
    else:
        user.gestor = MagicMock()
        user.gestor.nome_completo = "Gestor Mock"

    if not has_professor:
        del user.professor
    else:
        user.professor = MagicMock()
        user.professor.nome_completo = "Professor Mock"

    if not has_aluno:
        del user.aluno
    else:
        user.aluno = MagicMock()
        user.aluno.nome_completo = "Aluno Mock"

    return user


# ===========================================================================
# 1. is_super_ou_gestor
# ===========================================================================

class IsSuperOuGestorTest(TestCase):
    """Cobre todos os 4 branches da função corrigida."""

    def _call(self, user):
        from core.views import is_super_ou_gestor
        return is_super_ou_gestor(user)

    def test_superuser_ativo_retorna_true(self):
        user = MagicMock(is_active=True, is_superuser=True)
        del user.gestor
        self.assertTrue(self._call(user))

    def test_gestor_ativo_retorna_true(self):
        user = MagicMock(is_active=True, is_superuser=False)
        user.gestor = MagicMock()
        self.assertTrue(self._call(user))

    def test_superuser_inativo_retorna_false(self):
        """A versão corrigida exige is_active=True."""
        user = MagicMock(is_active=False, is_superuser=True)
        del user.gestor
        self.assertFalse(self._call(user))

    def test_usuario_comum_retorna_false(self):
        user = MagicMock(is_active=True, is_superuser=False)
        # hasattr retorna False quando o atributo não existe no spec
        del user.gestor
        self.assertFalse(self._call(user))


# ===========================================================================
# 2. get_foto_perfil
# ===========================================================================

class GetFotoPerfilTest(TestCase):
    """Cobre todos os branches da versão corrigida (iteração por tipo)."""

    def _call(self, user):
        from core.views import get_foto_perfil
        return get_foto_perfil(user)

    def _user_com_foto(self, tipo):
        user = MagicMock()
        perfil = MagicMock()
        perfil.foto = MagicMock()
        perfil.foto.url = f"/media/{tipo}.jpg"
        setattr(user, tipo, perfil)
        # Remove os outros tipos para não interferir
        for outro in ["professor", "aluno", "gestor"]:
            if outro != tipo:
                delattr(user, outro) if hasattr(user, outro) else None
        return user

    def test_retorna_url_foto_professor(self):
        user = MagicMock()
        user.professor = MagicMock()
        user.professor.foto = MagicMock()
        user.professor.foto.url = "/media/prof.jpg"
        del user.aluno
        del user.gestor
        self.assertEqual(self._call(user), "/media/prof.jpg")

    def test_retorna_url_foto_aluno(self):
        user = MagicMock()
        del user.professor
        user.aluno = MagicMock()
        user.aluno.foto = MagicMock()
        user.aluno.foto.url = "/media/aluno.jpg"
        del user.gestor
        self.assertEqual(self._call(user), "/media/aluno.jpg")

    def test_retorna_url_foto_gestor(self):
        user = MagicMock()
        del user.professor
        del user.aluno
        user.gestor = MagicMock()
        user.gestor.foto = MagicMock()
        user.gestor.foto.url = "/media/gest.jpg"
        self.assertEqual(self._call(user), "/media/gest.jpg")

    def test_retorna_none_sem_foto(self):
        user = MagicMock()
        user.professor = MagicMock()
        user.professor.foto = None
        del user.aluno
        del user.gestor
        result = self._call(user)
        self.assertIsNone(result)

    def test_retorna_none_sem_nenhum_perfil(self):
        user = MagicMock()
        del user.professor
        del user.aluno
        del user.gestor
        self.assertIsNone(self._call(user))

    def test_exception_no_perfil_continua_para_proximo(self):
        """Se um perfil lançar exceção, deve tentar o próximo."""
        user = MagicMock()
        user.professor = MagicMock()
        type(user.professor).foto = PropertyMock(side_effect=Exception("DB error"))
        user.aluno = MagicMock()
        user.aluno.foto = MagicMock()
        user.aluno.foto.url = "/media/aluno.jpg"
        del user.gestor
        self.assertEqual(self._call(user), "/media/aluno.jpg")


# ===========================================================================
# 3. get_nome_exibicao
# ===========================================================================

class GetNomeExibicaoTest(TestCase):
    """Cobre todos os branches da versão corrigida."""

    def _call(self, user):
        from core.views import get_nome_exibicao
        return get_nome_exibicao(user)

    def test_retorna_nome_gestor(self):
        user = MagicMock()
        user.gestor = MagicMock(nome_completo="Ana Gestora")
        self.assertEqual(self._call(user), "Ana Gestora")

    def test_retorna_nome_professor_quando_sem_gestor(self):
        user = MagicMock()
        del user.gestor
        user.professor = MagicMock(nome_completo="Carlos Prof")
        del user.aluno
        self.assertEqual(self._call(user), "Carlos Prof")

    def test_retorna_nome_aluno_quando_sem_gestor_e_professor(self):
        user = MagicMock()
        del user.gestor
        del user.professor
        user.aluno = MagicMock(nome_completo="Maria Aluna")
        self.assertEqual(self._call(user), "Maria Aluna")

    def test_retorna_first_last_name_quando_sem_perfil(self):
        user = MagicMock()
        del user.gestor
        del user.professor
        del user.aluno
        user.first_name = "João"
        user.last_name = "Silva"
        user.email = "joao@test.com"
        self.assertEqual(self._call(user), "João Silva")

    def test_retorna_email_quando_sem_nome_e_sem_perfil(self):
        user = MagicMock()
        del user.gestor
        del user.professor
        del user.aluno
        user.first_name = ""
        user.last_name = ""
        user.email = "usuario@test.com"
        self.assertEqual(self._call(user), "usuario@test.com")

    def test_perfil_sem_nome_completo_cai_para_proximo(self):
        user = MagicMock()
        user.gestor = MagicMock()
        user.gestor.nome_completo = None  # nome_completo falsy
        user.professor = MagicMock(nome_completo="Prof Válido")
        del user.aluno
        self.assertEqual(self._call(user), "Prof Válido")


# ===========================================================================
# 4. _calcular_situacao_nota_freq  (ex-_calcular_situacao_aluno versão 1)
# ===========================================================================

class CalcularSituacaoNotaFreqTest(TestCase):
    """Testa a função renomeada que recebe (media_final, frequencia_percentual)."""

    def _call(self, media, freq):
        from core.views import _calcular_situacao_nota_freq
        return _calcular_situacao_nota_freq(media, freq)

    def test_reprovado_por_falta(self):
        resultado = self._call(media=8.0, freq=74.9)
        self.assertEqual(resultado["texto"], "Reprovado por Falta")
        self.assertFalse(resultado["aprovado"])

    def test_aprovado(self):
        resultado = self._call(media=7.0, freq=75.0)
        self.assertEqual(resultado["texto"], "Aprovado")
        self.assertTrue(resultado["aprovado"])

    def test_recuperacao(self):
        resultado = self._call(media=6.0, freq=80.0)
        self.assertEqual(resultado["texto"], "Recuperação")
        self.assertFalse(resultado["aprovado"])

    def test_reprovado_por_nota(self):
        resultado = self._call(media=4.9, freq=80.0)
        self.assertEqual(resultado["texto"], "Reprovado")
        self.assertFalse(resultado["aprovado"])

    def test_media_exatamente_na_borda_recuperacao(self):
        resultado = self._call(media=5.0, freq=75.0)
        self.assertEqual(resultado["texto"], "Recuperação")

    def test_frequencia_exatamente_no_minimo(self):
        resultado = self._call(media=7.0, freq=75.0)
        self.assertEqual(resultado["texto"], "Aprovado")


# ===========================================================================
# 5. _calcular_situacao_aluno  (versão 2 — usada por painel_aluno)
# ===========================================================================

class CalcularSituacaoAlunoTest(TestCase):
    """Testa a versão que recebe (disciplinas_com_notas, total_lancadas, total_possiveis)."""

    def _call(self, disciplinas, lancadas, possiveis):
        from core.views import _calcular_situacao_aluno
        return _calcular_situacao_aluno(disciplinas, lancadas, possiveis)

    def _nota_mock(self, media):
        nota = MagicMock()
        nota.media = media
        return nota

    def test_sem_dados_quando_possiveis_zero(self):
        situacao, classe = self._call([], 0, 0)
        self.assertEqual(situacao, "Sem Dados")
        self.assertEqual(classe, "info")

    def test_cursando_quando_sem_medias(self):
        disc = [{"nota": None}]
        situacao, classe = self._call(disc, 0, 4)
        self.assertEqual(situacao, "Cursando")
        self.assertEqual(classe, "warning")

    def test_aprovado_media_igual_a_7(self):
        nota = self._nota_mock(7.0)
        disc = [{"nota": nota}]
        situacao, classe = self._call(disc, 4, 4)
        self.assertEqual(situacao, "Aprovado")
        self.assertEqual(classe, "success")

    def test_aprovado_media_acima_de_7(self):
        nota = self._nota_mock(9.5)
        disc = [{"nota": nota}]
        situacao, classe = self._call(disc, 4, 4)
        self.assertEqual(situacao, "Aprovado")

    def test_recuperacao_media_entre_5_e_7(self):
        nota = self._nota_mock(6.0)
        disc = [{"nota": nota}]
        situacao, classe = self._call(disc, 4, 4)
        self.assertEqual(situacao, "Recuperação")
        self.assertEqual(classe, "warning")

    def test_reprovado_media_abaixo_de_5(self):
        nota = self._nota_mock(3.0)
        disc = [{"nota": nota}]
        situacao, classe = self._call(disc, 4, 4)
        self.assertEqual(situacao, "Reprovado")
        self.assertEqual(classe, "danger")

    def test_media_none_e_nota_presente_ignorada(self):
        nota = self._nota_mock(None)
        disc = [{"nota": nota}]
        situacao, classe = self._call(disc, 4, 4)
        self.assertEqual(situacao, "Cursando")

    def test_media_calculada_com_multiplas_disciplinas(self):
        """Média de 6 (recuperação) com duas disciplinas."""
        disc = [
            {"nota": self._nota_mock(5.0)},
            {"nota": self._nota_mock(7.0)},
        ]
        situacao, _ = self._call(disc, 8, 8)
        self.assertEqual(situacao, "Recuperação")


# ===========================================================================
# 6. login_view  (versão corrigida — mantida a 2ª)
# ===========================================================================

class LoginViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("login")

    def test_get_renderiza_formulario(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertIn("form", response.context)

    def test_usuario_autenticado_e_redirecionado(self):
        user = User.objects.create_user(
            username="12345678900", email="auth@test.com", password="senha123"
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [301, 302])

    def test_post_credenciais_invalidas_renderiza_form_com_erro(self):
        response = self.client.post(self.url, {
            "email": "naoexiste@test.com",
            "password": "errada"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_post_campos_vazios_renderiza_form(self):
        response = self.client.post(self.url, {"email": "", "password": ""})
        self.assertEqual(response.status_code, 200)

    def test_post_credenciais_validas_redireciona(self):
        User.objects.create_user(
            username="99988877766",
            email="valido@test.com",
            password="senha123"
        )
        response = self.client.post(self.url, {
            "email": "valido@test.com",
            "password": "senha123"
        })
        self.assertIn(response.status_code, [301, 302])


# ===========================================================================
# 7. logout_view  (versão corrigida — sem message, só redirect)
# ===========================================================================

class LogoutViewTest(TestCase):

    def test_logout_redireciona_para_login(self):
        user = User.objects.create_user(
            username="logout_user", email="lo@test.com", password="senha123"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"),
                             fetch_redirect_response=False)

    def test_logout_encerra_sessao(self):
        user = User.objects.create_user(
            username="session_user", email="s@test.com", password="senha123"
        )
        self.client.force_login(user)
        self.client.get(reverse("logout"))
        # Após logout, acesso a área restrita deve redirecionar para login
        response = self.client.get(reverse("painel_super"))
        self.assertIn(response.status_code, [301, 302])

    def test_logout_sem_mensagem_residual(self):
        """Versão corrigida NÃO deve adicionar messages.info."""
        user = User.objects.create_user(
            username="msg_user", email="msg@test.com", password="senha123"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("logout"), follow=True)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 0)


# ===========================================================================
# 8. _contar_notas_lancadas  (versão corrigida — aggregate por bimestre)
# ===========================================================================

class ContarNotasLancadasTest(TestCase):

    def _call(self, disciplina, turma):
        from core.views import _contar_notas_lancadas
        return _contar_notas_lancadas(disciplina, turma)

    @patch("core.views.Nota")
    def test_sem_notas_retorna_zero(self, MockNota):
        MockNota.objects.filter.return_value.aggregate.return_value = {
            "n1": 0, "n2": 0, "n3": 0, "n4": 0
        }
        resultado = self._call(MagicMock(), MagicMock())
        self.assertEqual(resultado, 0)

    @patch("core.views.Nota")
    def test_contagem_de_todos_os_bimestres(self, MockNota):
        MockNota.objects.filter.return_value.aggregate.return_value = {
            "n1": 3, "n2": 3, "n3": 2, "n4": 1
        }
        resultado = self._call(MagicMock(), MagicMock())
        self.assertEqual(resultado, 9)

    @patch("core.views.Nota")
    def test_valores_none_sao_tratados_como_zero(self, MockNota):
        MockNota.objects.filter.return_value.aggregate.return_value = {
            "n1": None, "n2": 2, "n3": None, "n4": 1
        }
        resultado = self._call(MagicMock(), MagicMock())
        self.assertEqual(resultado, 3)

    @patch("core.views.Nota")
    def test_todos_os_bimestres_preenchidos(self, MockNota):
        MockNota.objects.filter.return_value.aggregate.return_value = {
            "n1": 30, "n2": 30, "n3": 30, "n4": 30
        }
        resultado = self._call(MagicMock(), MagicMock())
        self.assertEqual(resultado, 120) 
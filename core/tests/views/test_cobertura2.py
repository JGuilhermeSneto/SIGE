"""
Testes para as linhas restantes — categorias B e C.
Cobre: _get_grade_formatada, _get_ocupados_por_professor,
get_foto_perfil (exception branch), branches de views diversas.
"""

from unittest.mock import MagicMock, patch, PropertyMock
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()


# ==================== _formatar_nota (antigo _get_grade_formatada) ====================
class GetGradeFormatadasTest(TestCase):
    def _call(self, valor):
        from core.views import _formatar_nota
        return _formatar_nota(valor)

    def test_none_retorna_traco_e_muted(self):
        r = self._call(None)
        self.assertEqual(r["valor"], "-")
        self.assertEqual(r["classe"], "text-muted")

    def test_nota_aprovado(self):
        r = self._call(8.0)
        self.assertIn("success", r["classe"])
        self.assertEqual(r["valor"], "8.0")

    def test_nota_recuperacao(self):
        r = self._call(6.0)
        self.assertIn("warning", r["classe"])

    def test_nota_reprovado(self):
        r = self._call(3.0)
        self.assertIn("danger", r["classe"])

    def test_nota_exatamente_7(self):
        r = self._call(7.0)
        self.assertIn("success", r["classe"])

    def test_nota_exatamente_5(self):
        r = self._call(5.0)
        self.assertIn("warning", r["classe"])

    def test_string_invalida_retorna_traco(self):
        r = self._call("abc")
        self.assertEqual(r["valor"], "-")
        self.assertEqual(r["classe"], "text-muted")

    def test_string_numerica_valida(self):
        r = self._call("9.5")
        self.assertEqual(r["valor"], "9.5")


# =============================================================
# _get_ocupados_por_professor  (linhas 132-159)
# =============================================================

class GetOcupadosPorProfessorTest(TestCase):
    def _call(self, professor_id, ano_letivo, turma_id_atual=None):
        from core.views import _get_ocupados_por_professor
        return _get_ocupados_por_professor(professor_id, ano_letivo, turma_id_atual)

    @patch("core.views.GradeHorario.objects.filter")
    def test_sem_registros_retorna_set_vazio(self, mock_filter):
        mock_filter.return_value.select_related.return_value = []
        resultado = self._call(1, 2024)
        self.assertEqual(resultado, set())

    @patch("core.views.GradeHorario.objects.filter")
    def test_conflito_detectado(self, mock_filter):
        # Mock de um registro de grade
        registro = MagicMock()
        registro.dia = "segunda"
        registro.horario = "07:00 às 07:45"
        registro.turma.turno = "manha"
        registro.disciplina.professor.id = 5
        
        mock_filter.return_value.select_related.return_value = [registro]
        resultado = self._call(5, 2024)
        self.assertIn("segunda-0", resultado)

    @patch("core.views.GradeHorario.objects.filter")
    def test_exclui_turma_atual(self, mock_filter):
        self._call(1, 2024, turma_id_atual=10)
        mock_filter.return_value.select_related.return_value.exclude.assert_called_with(turma_id=10)


# =============================================================
# get_foto_perfil — branch de exception (linhas 252-254)
# =============================================================

class GetFotoPerfilExceptionBranchTest(TestCase):

    def test_todos_perfis_com_exception_retorna_none(self):
        from core.views import get_foto_perfil
        user = MagicMock()
        # Todos os tipos lançam exceção ao acessar .foto
        for tipo in ["professor", "aluno", "gestor"]:
            perfil = MagicMock()
            type(perfil).foto = PropertyMock(side_effect=Exception("fail"))
            setattr(user, tipo, perfil)
        resultado = get_foto_perfil(user)
        self.assertIn("default-user.png", resultado)


# =============================================================
# painel_super — branches de ano_filtro (linhas ~475, 477)
# =============================================================

class PainelSuperAnoBranchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="super", email="super@test.com", password="senha123"
        )
        self.client.force_login(self.user)

    def test_sem_turmas_usa_ano_atual(self):
        response = self.client.get("/painel/super/")
        self.assertEqual(response.status_code, 200)

    def test_ano_invalido_na_query_string(self):
        response = self.client.get("/painel/super/?ano=abc")
        self.assertEqual(response.status_code, 200)

    def test_ano_valido_na_query_string(self):
        response = self.client.get("/painel/super/?ano=2023")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ano_filtro"], 2023)


# =============================================================
# listar_turmas — branch de query vazia vs com texto (548-549)
# =============================================================

class ListarTurmasBranchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="super2", email="s2@test.com", password="senha123"
        )
        self.client.force_login(self.user)

    def test_sem_query_lista_tudo(self):
        response = self.client.get("/turmas/")
        self.assertEqual(response.status_code, 200)

    def test_com_query_filtra(self):
        response = self.client.get("/turmas/?q=9A")
        self.assertEqual(response.status_code, 200)


# =============================================================
# cadastrar_turma — branches de erro (linhas 587-590)
# =============================================================

class CadastrarTurmaBranchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="super3", email="s3@test.com", password="senha123"
        )
        self.client.force_login(self.user)

    def test_ano_fora_do_range_exibe_erro(self):
        response = self.client.post("/turmas/cadastrar/", {
            "nome": "9A", "turno": "manha", "ano": "1990"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("erro", response.context)

    def test_ano_string_invalida_exibe_erro(self):
        response = self.client.post("/turmas/cadastrar/", {
            "nome": "9A", "turno": "manha", "ano": "não_é_número"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("erro", response.context)

    def test_turma_duplicada_exibe_erro(self):
        from core.models import Turma
        Turma.objects.create(nome="9A", turno="manha", ano=2024)
        response = self.client.post("/turmas/cadastrar/", {
            "nome": "9A", "turno": "manha", "ano": "2024"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("erro", response.context)

    def test_turma_valida_redireciona(self):
        response = self.client.post("/turmas/cadastrar/", {
            "nome": "8B", "turno": "tarde", "ano": "2024"
        })
        self.assertRedirects(response, "/turmas/", fetch_redirect_response=False)


# =============================================================
# _calcular_situacao_aluno v2 — branches não cobertos (1739-1746)
# =============================================================

class CalcularSituacaoAlunoBordaTest(TestCase):

    def _call(self, disciplinas, lancadas, possiveis):
        from core.views import _calcular_situacao_aluno
        return _calcular_situacao_aluno(disciplinas, lancadas, possiveis)

    def test_media_exatamente_5(self):
        nota = MagicMock()
        nota.media = 5.0
        situacao, _ = self._call([{"nota": nota}], 4, 4)
        self.assertEqual(situacao, "Recuperação")

    def test_media_exatamente_7(self):
        nota = MagicMock()
        nota.media = 7.0
        situacao, _ = self._call([{"nota": nota}], 4, 4)
        self.assertEqual(situacao, "Aprovado")

    def test_mistura_nota_none_e_valida(self):
        """Disciplinas com nota=None são ignoradas na média."""
        nota_valida = MagicMock()
        nota_valida.media = 8.0
        disc = [{"nota": None}, {"nota": nota_valida}]
        situacao, _ = self._call(disc, 8, 8)
        self.assertEqual(situacao, "Aprovado")


# =============================================================
# painel_aluno — branches de acesso negado (linhas 1802-1803)
# =============================================================

class PainelAlunoBranchTest(TestCase):

    def test_usuario_sem_perfil_aluno_e_redirecionado(self):
        user = User.objects.create_user(
            username="naoaluno", email="na@test.com", password="senha123"
        )
        self.client.force_login(user)
        response = self.client.get("/painel/aluno/")
        self.assertIn(response.status_code, [302, 301])


# =============================================================
# frequencia_aluno — branch de acesso negado (linhas ~1897-1900)
# =============================================================

class FrequenciaAlunoBranchTest(TestCase):

    def test_nao_aluno_e_redirecionado(self):
        user = User.objects.create_user(
            username="prof_freq", email="pf@test.com", password="senha123"
        )
        self.client.force_login(user)
        response = self.client.get("/frequencia/aluno/")
        self.assertIn(response.status_code, [302, 301])


# =============================================================
# Forms — linhas 149, 173 (ProfessorForm), 362, 384 (GestorForm)
# =============================================================

class FormsBranchesTest(TestCase):
    """
    Linhas 149 e 173 são o branch de `if senha and len(senha) < 6`
    no ProfessorForm e AlunoForm. Linhas 362 e 384 são o mesmo
    branch no GestorForm.
    """

    def _base_data(self):
        return {
            "nome_completo": "Teste",
            "cpf": "123.456.789-00",
            "data_nascimento": "1990-01-01",
            "telefone": "84999999999",
            "email": "t@test.com",
            "senha": "123",           # <- senha curta para acionar o branch
            "senha_confirmacao": "123",
        }

    def test_professor_form_senha_curta(self):
        from core.forms import ProfessorForm
        data = self._base_data()
        form = ProfessorForm(data=data)
        self.assertFalse(form.is_valid())
        erros = str(form.errors)
        self.assertIn("mínimo 6", erros)

    def test_aluno_form_senha_curta(self):
        from core.forms import AlunoForm
        data = self._base_data()
        form = AlunoForm(data=data)
        self.assertFalse(form.is_valid())
        erros = str(form.errors)
        self.assertIn("mínimo 6", erros)

    def test_gestor_form_senha_curta(self):
        from core.forms import GestorForm
        data = self._base_data()
        form = GestorForm(data=data)
        self.assertFalse(form.is_valid())
        erros = str(form.errors)
        self.assertIn("mínimo 6", erros)

    def test_gestor_form_senhas_divergentes(self):
        from core.forms import GestorForm
        data = self._base_data()
        data["senha"] = "senha_longa_ok"
        data["senha_confirmacao"] = "senha_diferente"
        form = GestorForm(data=data)
        self.assertFalse(form.is_valid())


# =============================================================
# models.py linha 433 — branch de __str__ ou método de model
# (ajuste o teste abaixo de acordo com o que está na linha 433)
# =============================================================

class ModelsBranchTest(TestCase):

    def test_modelo_linha_433(self):
        """
        Inspecione core/models.py linha 433 e escreva o teste
        específico aqui. Geralmente é um método __str__, property,
        ou branch de validação. Exemplo genérico:
        """
        # from core.models import SeuModelo
        # obj = SeuModelo(campo="valor")
        # self.assertEqual(str(obj), "valor esperado")
        pass  # <- substituir pelo teste real após inspecionar a linha

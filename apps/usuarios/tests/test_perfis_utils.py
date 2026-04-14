from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.academico.models.academico import Turma
from apps.usuarios.models.perfis import Aluno, Gestor, Professor
from apps.usuarios.utils.perfis import (
    get_foto_perfil,
    get_nome_exibicao,
    get_user_profile,
    is_super_ou_gestor,
    redirect_user,
)

User = get_user_model()


class PerfisUtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario", email="usuario@example.com", password="senha123"
        )

    def test_get_nome_exibicao_retorna_nome_completo_e_email(self):
        self.user.first_name = "João"
        self.user.last_name = "Silva"
        self.user.save()

        self.assertEqual(get_nome_exibicao(self.user), "João Silva")

        user_sem_nome = User.objects.create_user(
            username="semnome", email="semnome@example.com", password="senha123"
        )
        self.assertEqual(get_nome_exibicao(user_sem_nome), "semnome@example.com")

    def test_get_user_profile_retorna_perfil_correto(self):
        gestor = Gestor.objects.create(
            user=self.user,
            nome_completo="Gestor Teste",
            cpf="222.333.444-55",
            data_nascimento="1980-01-01",
            cargo="diretor",
        )
        self.assertEqual(get_user_profile(self.user), gestor)

        professor_user = User.objects.create_user(
            username="profuser", email="profuser@example.com", password="senha123"
        )
        professor = Professor.objects.create(
            user=professor_user,
            nome_completo="Professor Teste",
            cpf="333.444.555-66",
            data_nascimento="1985-01-01",
        )
        self.assertEqual(get_user_profile(professor_user), professor)

        aluno_user = User.objects.create_user(
            username="alunouser", email="alunouser@example.com", password="senha123"
        )
        turma = Turma.objects.create(nome="2B", turno="tarde", ano=2024)
        aluno = Aluno.objects.create(
            user=aluno_user,
            nome_completo="Aluno Teste",
            cpf="444.555.666-77",
            data_nascimento="2010-01-01",
            turma=turma,
        )
        self.assertEqual(get_user_profile(aluno_user), aluno)

        user_sem_perfil = User.objects.create_user(
            username="semperfil", email="semperfil@example.com", password="senha123"
        )
        self.assertIsNone(get_user_profile(user_sem_perfil))

    def test_get_foto_perfil_retorna_url_da_imagem_ou_padrao(self):
        user_sem_foto = User.objects.create_user(
            username="semfoto", email="semfoto@example.com", password="senha123"
        )
        gestor = Gestor.objects.create(
            user=user_sem_foto,
            nome_completo="Gestor Foto",
            cpf="555.666.777-88",
            data_nascimento="1975-01-01",
            cargo="diretor",
        )
        resultado_padrao = get_foto_perfil(user_sem_foto)
        self.assertTrue(resultado_padrao.endswith("core/img/default-user.png"))

        user_com_foto = User.objects.create_user(
            username="comfoto", email="comfoto@example.com", password="senha123"
        )
        professor = Professor.objects.create(
            user=user_com_foto,
            nome_completo="Professor Foto",
            cpf="666.777.888-99",
            data_nascimento="1982-01-01",
        )
        professor.foto = SimpleUploadedFile(
            "perfil.jpg", b"fake-image-content", content_type="image/jpeg"
        )
        professor.save()

        resultado_foto = get_foto_perfil(user_com_foto)
        self.assertIn("fotos/pessoas", resultado_foto)
        self.assertFalse(resultado_foto.endswith("core/img/default-user.png"))

    def test_redirect_user_escolhe_rota_corretamente(self):
        superuser = User.objects.create_superuser(
            username="super", email="super@example.com", password="senha123"
        )
        self.assertEqual(redirect_user(superuser), "painel_super")

        gestor_user = User.objects.create_user(
            username="gestor", email="gestor@example.com", password="senha123"
        )
        Gestor.objects.create(
            user=gestor_user,
            nome_completo="Gestor Redireciona",
            cpf="777.888.999-00",
            data_nascimento="1978-01-01",
            cargo="diretor",
        )
        self.assertEqual(redirect_user(gestor_user), "painel_gestor")

        professor_user = User.objects.create_user(
            username="professor2", email="prof2@example.com", password="senha123"
        )
        Professor.objects.create(
            user=professor_user,
            nome_completo="Prof Redireciona",
            cpf="888.999.000-11",
            data_nascimento="1985-01-01",
        )
        self.assertEqual(redirect_user(professor_user), "painel_professor")

        aluno_user = User.objects.create_user(
            username="aluno2", email="aluno2@example.com", password="senha123"
        )
        turma = Turma.objects.create(nome="3C", turno="noite", ano=2024)
        Aluno.objects.create(
            user=aluno_user,
            nome_completo="Aluno Redireciona",
            cpf="999.000.111-22",
            data_nascimento="2010-01-01",
            turma=turma,
        )
        self.assertEqual(redirect_user(aluno_user), "painel_aluno")

        usuario_sem_perfil = User.objects.create_user(
            username="semperfil2", email="semperfil2@example.com", password="senha123"
        )
        self.assertEqual(redirect_user(usuario_sem_perfil), "painel_usuarios")

    def test_is_super_ou_gestor_reconhece_perfis(self):
        superuser = User.objects.create_superuser(
            username="super2", email="super2@example.com", password="senha123"
        )
        self.assertTrue(is_super_ou_gestor(superuser))

        gestor_user = User.objects.create_user(
            username="gestor2", email="gestor2@example.com", password="senha123"
        )
        Gestor.objects.create(
            user=gestor_user,
            nome_completo="Gestor Teste 2",
            cpf="111.222.333-88",
            data_nascimento="1977-01-01",
            cargo="diretor",
        )
        self.assertTrue(is_super_ou_gestor(gestor_user))

        professor_user = User.objects.create_user(
            username="professor3", email="prof3@example.com", password="senha123"
        )
        Professor.objects.create(
            user=professor_user,
            nome_completo="Prof Teste 3",
            cpf="222.333.444-99",
            data_nascimento="1983-01-01",
        )
        self.assertFalse(is_super_ou_gestor(professor_user))

        aluno_user = User.objects.create_user(
            username="aluno3", email="aluno3@example.com", password="senha123"
        )
        turma = Turma.objects.create(nome="4D", turno="manha", ano=2024)
        Aluno.objects.create(
            user=aluno_user,
            nome_completo="Aluno Teste 3",
            cpf="333.444.555-00",
            data_nascimento="2010-01-01",
            turma=turma,
        )
        self.assertFalse(is_super_ou_gestor(aluno_user))

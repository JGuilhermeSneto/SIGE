from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.usuarios.models.perfis import Gestor
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class PerfisViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "senha123"
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password=self.password
        )
        self.perfil = Gestor.objects.create(
            user=self.user,
            nome_completo="Test User",
            cpf="272.766.190-26",
            data_nascimento="1980-01-01",
        )
        self.client.force_login(self.user)

    def test_editar_perfil_get(self):
        response = self.client.get(reverse("editar_perfil"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/editar_perfil.html")

    def test_remover_foto_perfil(self):
        self.perfil.foto = SimpleUploadedFile(
            "foto.jpg", b"content", content_type="image/jpeg"
        )
        self.perfil.save()

        response = self.client.get(reverse("remover_foto_perfil"))
        self.perfil.refresh_from_db()
        self.assertFalse(bool(self.perfil.foto))
        self.assertRedirects(response, reverse("editar_perfil"))

    def test_atualizar_foto_perfil_ajax(self):
        foto = SimpleUploadedFile(
            "nova_foto.jpg", b"new_content", content_type="image/jpeg"
        )
        response = self.client.post(
            reverse("atualizar_foto_perfil"),
            {"foto": foto},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("foto_url", response.json())

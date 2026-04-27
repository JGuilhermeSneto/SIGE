import pytest
from django.urls import reverse
from apps.comum.tests.factories import ResponsavelFactory, AlunoFactory

@pytest.mark.django_db
class TestPainelResponsavel:
    def test_acesso_painel_responsavel(self, client):
        # Cria um responsável e loga
        responsavel = ResponsavelFactory()
        client.force_login(responsavel.user)
        
        # Cria um dependente e vincula
        aluno = AlunoFactory()
        responsavel.alunos.add(aluno)
        
        url = reverse("painel_responsavel")
        response = client.get(url)
        
        assert response.status_code == 200
        assert aluno.nome_completo in response.content.decode("utf-8")
        assert "Portal do Responsável" in response.content.decode("utf-8")

    def test_responsavel_ve_detalhes_filho(self, client):
        responsavel = ResponsavelFactory()
        client.force_login(responsavel.user)
        
        aluno = AlunoFactory()
        responsavel.alunos.add(aluno)
        
        # Tenta acessar o painel do aluno com o ID dele
        url = reverse("painel_aluno") + f"?aluno_id={aluno.id}"
        response = client.get(url)
        
        assert response.status_code == 200
        assert aluno.nome_completo in response.content.decode("utf-8")

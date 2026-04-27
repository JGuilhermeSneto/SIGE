import factory
from django.contrib.auth.models import User
from apps.comum.models.tenant import Instituicao
from apps.usuarios.models.perfis import Aluno, Responsavel
from apps.academico.models.academico import Turma

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

class InstituicaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instituicao

    nome = factory.Faker("company")
    cnpj = factory.Sequence(lambda n: f"00.000.000/0001-{n:02d}")
    slug = factory.Faker("slug")
    ativo = True

class TurmaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Turma
    
    nome = factory.Faker("word")
    ano = 2026
    turno = "MATUTINO"

class AlunoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aluno
    
    user = factory.SubFactory(UserFactory)
    nome_completo = factory.Faker("name")
    cpf = factory.Sequence(lambda n: f"{n:011d}")
    turma = factory.SubFactory(TurmaFactory)

class ResponsavelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Responsavel
    
    user = factory.SubFactory(UserFactory)
    nome_completo = factory.Faker("name")
    cpf = factory.Sequence(lambda n: f"{n:011d}")
    parentesco = "Pai"

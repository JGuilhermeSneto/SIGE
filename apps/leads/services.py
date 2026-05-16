from django.db import transaction
from django.contrib.auth.models import User
from apps.usuarios.models.perfis import Aluno
from apps.academico.models import Turma
from .models import Lead

class LeadService:
    @staticmethod
    @transaction.atomic
    def converter_lead_em_aluno(lead_id, turma_id, senha_inicial="Sige123@"):
        """
        Converte um Lead em um Aluno real, criando usuário e perfil.
        """
        lead = Lead.objects.get(id=lead_id)
        turma = Turma.objects.get(id=turma_id)

        # 1. Criar Usuário (Username será o e-mail ou nome simplificado)
        username = lead.email if lead.email else lead.name.lower().replace(" ", ".")
        user = User.objects.create_user(
            username=username,
            email=lead.email,
            password=senha_inicial,
            first_name=lead.name.split(" ")[0]
        )

        # 2. Criar Perfil de Aluno
        aluno = Aluno.objects.create(
            user=user,
            nome_completo=lead.name,
            turma=turma,
            status_matricula="ATIVO"
        )

        # 3. Atualizar Lead no Funil (Supondo que exista uma etapa 'Matriculado')
        # Buscamos a etapa de maior ordem ou com nome similar
        from .models import FunnelStage
        stage_matriculado = FunnelStage.objects.filter(name__icontains="Matrícula").first()
        if stage_matriculado:
            lead.stage = stage_matriculado
            lead.save()

        return aluno

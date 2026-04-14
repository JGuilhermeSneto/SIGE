from ..models.academico import AtividadeProfessor, EntregaAtividade, Questao

class AtividadeSeletores:
    """Seletores para recuperar dados de atividades com lógica de filtragem e prefetch."""

    @staticmethod
    def buscar_atividade_com_questoes(atividade_id):
        """Busca uma atividade específica trazendo suas questões e alternativas pré-carregadas."""
        return AtividadeProfessor.objects.prefetch_related(
            'questoes__alternativas'
        ).get(id=atividade_id)

    @staticmethod
    def buscar_entregas_por_atividade(atividade_id):
        """Retorna todas as entregas de uma atividade com dados do aluno."""
        return EntregaAtividade.objects.filter(
            atividade_id=atividade_id
        ).select_related('aluno__user').order_by('aluno__nome_completo')

    @staticmethod
    def buscar_entrega_detalhada(entrega_id):
        """Busca uma entrega específica com suas respostas e questões relacionadas."""
        return EntregaAtividade.objects.select_related(
            'aluno__user', 'atividade'
        ).prefetch_related(
            'respostas__questao', 
            'atividade__questoes__alternativas'
        ).get(id=entrega_id)

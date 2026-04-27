from django.db.models import Prefetch
from ..models.academico import Disciplina, PlanejamentoAula, MaterialDidatico
from ..models.desempenho import Nota, Frequencia

class DesempenhoSelector:
    @staticmethod
    def get_resumo_academico_aluno(aluno):
        """
        Recupera todo o histórico acadêmico do aluno de forma otimizada.
        Reduz consultas N+1 para O(1) ou O(constante).
        """
        # Prefetch de notas e frequências
        notas_qs = Nota.objects.filter(aluno=aluno)
        frequencias_qs = Frequencia.objects.filter(aluno=aluno)
        
        # Prefetch de planejamentos e materiais (limitados aos últimos 5/3)
        # Nota: Prefetch não suporta slicing direto facilmente, mas podemos pré-filtrar
        
        disciplinas = Disciplina.objects.filter(turma=aluno.turma).select_related('professor').prefetch_related(
            Prefetch('notas', queryset=notas_qs, to_attr='nota_aluno_prefetched'),
            Prefetch('frequencias', queryset=frequencias_qs, to_attr='frequencias_aluno_prefetched')
        )
        
        return disciplinas

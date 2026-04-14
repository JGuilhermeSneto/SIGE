"""
Regras de negócio transacionais: entrega de atividade, respostas, notas de atividade.

O que é: camada de serviço chamada pelas views para persistir vários modelos
de forma consistente.
"""

from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models.academico import (
    AtividadeProfessor, EntregaAtividade, RespostaAluno, 
    Questao, Alternativa
)
from ..models.desempenho import NotaAtividade
from .notificacao_servico import NotificacaoServico

class AtividadeServico:
    """Serviço para gerenciar lógica de negócios de atividades e avaliações."""

    @staticmethod
    def processar_entrega_aluno(aluno, atividade_id, data_post, arquivos):
        """Processa a entrega de um aluno, salvando arquivo e respostas do quiz."""
        atividade = AtividadeProfessor.objects.get(id=atividade_id)
        
        hoje = timezone.now()
        if atividade.prazo_final and hoje > atividade.prazo_final:
            raise ValueError("O prazo para esta atividade já se encerrou.")

        entrega, _ = EntregaAtividade.objects.get_or_create(aluno=aluno, atividade=atividade)
        
        # Upload de Arquivo
        arquivo = arquivos.get("arquivo")
        if arquivo:
            entrega.arquivo = arquivo
        
        entrega.comentario_aluno = data_post.get("comentario", "")
        entrega.status = 'ENTREGUE'
        entrega.save()

        # Respostas das Questões
        questoes = atividade.questoes.all()
        for q in questoes:
            if q.tipo == 'OBJETIVA':
                alt_id = data_post.get(f'questao_{q.id}')
                if alt_id:
                    alt = get_object_or_404(Alternativa, id=alt_id, questao=q)
                    RespostaAluno.objects.update_or_create(
                        entrega=entrega, questao=q,
                        defaults={'alternativa_escolhida': alt}
                    )
            else: # DISCURSIVA
                texto = data_post.get(f'questao_{q.id}')
                if texto:
                    RespostaAluno.objects.update_or_create(
                        entrega=entrega, questao=q,
                        defaults={'texto_resposta': texto}
                    )
        return entrega

    @staticmethod
    def salvar_banco_questoes(atividade, data_post):
        """Recria o banco de questões de uma atividade com base nos dados do formulário."""
        questoes_count = int(data_post.get("questoes_count", 0))
        if atividade.tipo == "PROVA" and questoes_count == 0:
            raise ValueError("Provas precisam ter ao menos uma questão de gabarito.")

        saved_questions = 0
        with transaction.atomic():
            Questao.objects.filter(atividade=atividade).delete()
            for i in range(1, questoes_count + 1):
                texto = data_post.get(f"questao_texto_{i}")
                tipo = data_post.get(f"questao_tipo_{i}")
                valor = data_post.get(f"questao_valor_{i}", 1.0)
                
                if not texto:
                    continue

                q = Questao.objects.create(
                    atividade=atividade, texto=texto, tipo=tipo, valor=valor, ordem=i
                )
                saved_questions += 1

                if tipo == "OBJETIVA":
                    alternativa_correta_definida = False
                    alternativas_criadas = 0
                    for j in range(1, 6):
                        alt_texto = data_post.get(f"alt_{i}_{j}")
                        if alt_texto:
                            alternativas_criadas += 1
                            eh_correta = data_post.get(f"correta_{i}") == str(j)
                            if eh_correta:
                                alternativa_correta_definida = True
                            Alternativa.objects.create(questao=q, texto=alt_texto, eh_correta=eh_correta)

                    if alternativas_criadas == 0:
                        raise ValueError(f"Questão {i} objetiva precisa ter pelo menos uma alternativa.")
                    if not alternativa_correta_definida:
                        raise ValueError(f"Questão {i} objetiva precisa ter uma alternativa correta.")

            if atividade.tipo == "PROVA" and saved_questions == 0:
                raise ValueError("Provas precisam ter ao menos uma questão de gabarito.")

    @staticmethod
    def finalizar_correcao(entrega, data_post):
        """Finaliza a correção de uma entrega, atribuindo pontos e feedback."""
        atividade = entrega.atividade
        questoes = atividade.questoes.all()
        respostas = {r.questao_id: r for r in entrega.respostas.all()}
        
        total_pontos = 0
        for q in questoes:
            r = respostas.get(q.id)
            if not r:
                r = RespostaAluno.objects.create(entrega=entrega, questao=q)
            
            r.comentario_professor = data_post.get(f"feedback_{q.id}", "")
            
            if q.tipo == "OBJETIVA":
                if r.alternativa_escolhida and r.alternativa_escolhida.eh_correta:
                    r.pontos_atribuidos = q.valor
                else:
                    r.pontos_atribuidos = Decimal("0")
            else:
                val = data_post.get(f"pontos_{q.id}", 0)
                try:
                    r.pontos_atribuidos = Decimal(str(val).replace(",", "."))
                except (InvalidOperation, TypeError):
                    r.pontos_atribuidos = Decimal("0")

            r.save()
            total_pontos += r.pontos_atribuidos or Decimal("0")

        NotaAtividade.objects.update_or_create(
            aluno=entrega.aluno, atividade=atividade,
            defaults={"valor": total_pontos, "observacao": data_post.get("obs_geral", "")}
        )

        entrega.feedback_professor = data_post.get("obs_geral", "")
        entrega.status = data_post.get("status", "CORRIGIDO")
        entrega.save()
        NotificacaoServico.criar(
            aluno=entrega.aluno,
            tipo="CORRECAO",
            titulo="Correção disponível",
            mensagem=f"Sua entrega de '{atividade.titulo}' foi corrigida pelo professor.",
            url_destino=f"/academico/meu-painel/atividades/{atividade.id}/entregar/",
        )
        return total_pontos

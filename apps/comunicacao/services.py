from django.core.mail import send_mail
from django.conf import settings
from .models.comunicacao import Comunicado

class ComunicacaoService:
    @staticmethod
    def enviar_alerta_evasao(aluno, score, fatores):
        """Envia e-mail de alerta para os responsáveis do aluno."""
        assunto = f"Acompanhamento Pedagógico: {aluno.nome_completo}"
        mensagem = f"""
        Olá,
        
        Gostaríamos de agendar uma reunião para conversar sobre o desempenho acadêmico de {aluno.nome_completo}.
        Nosso sistema de inteligência detectou pontos de atenção que gostaríamos de discutir preventivamente.
        
        Motivo: {fatores}
        
        Atenciosamente,
        Coordenação SIGE Apex
        """
        
        # Simulação de envio (usa o e-mail do usuário associado ao aluno)
        email_destino = aluno.user.email
        if email_destino:
            send_mail(
                assunto,
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [email_destino],
                fail_silently=True,
            )
            return True
        return False

    @staticmethod
    def disparar_comunicado_geral(titulo, corpo, tipo="AVISO"):
        """Cria um comunicado no sistema para todos os usuários."""
        return Comunicado.objects.create(
            titulo=titulo,
            corpo=corpo,
            tipo=tipo
        )

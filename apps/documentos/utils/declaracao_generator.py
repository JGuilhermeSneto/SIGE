from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm
from .pdf_generator import InstitutionalPDF

class DeclaracaoGenerator(InstitutionalPDF):
    """
    Gerador especializado para a Declaração de Matrícula.
    """
    
    def __init__(self, buffer, aluno):
        super().__init__(buffer, title=f"Declaracao_{aluno.nome_completo}")
        self.aluno = aluno

    def generate(self):
        elements = []
        
        # Título
        elements.append(Paragraph("DECLARAÇÃO DE MATRÍCULA", self.styles['InstitutionalTitle']))
        elements.append(Spacer(1, 2*cm))
        
        # Texto da Declaração
        import locale
        from django.utils import timezone
        
        data_extenso = timezone.now().strftime("%d de %B de %Y")
        
        # Texto formatado
        texto = f"""
        Declaramos para os devidos fins que o(a) aluno(a) <b>{self.aluno.nome_completo.upper()}</b>, 
        portador(a) do CPF <b>{self.aluno.cpf}</b>, encontra-se regularmente matriculado(a) nesta 
        unidade de ensino, cursando a turma <b>{self.aluno.turma.nome}</b> no ano letivo de <b>{self.aluno.turma.ano}</b>.
        <br/><br/>
        O referido aluno possui situação de matrícula <b>{self.aluno.get_status_matricula_display()}</b>.
        <br/><br/>
        Esta declaração é válida por 30 dias a partir da data de sua emissão e pode ser validada através do QR Code 
        constante no rodapé deste documento.
        """
        
        elements.append(Paragraph(texto, self.styles['Normal']))
        elements.append(Spacer(1, 3*cm))
        
        # Local e Data
        elements.append(Paragraph(f"Natal-RN, {data_extenso}.", self.styles['Normal']))
        elements.append(Spacer(1, 4*cm))
        
        # Assinatura
        elements.append(Paragraph("____________________________________", self.styles['Normal']))
        elements.append(Paragraph("<b>Secretaria Acadêmica</b>", self.styles['Normal']))
        elements.append(Paragraph("SIGE - Sistema Integrado de Gestão Escolar", self.styles['Normal']))
        
        # Constrói o PDF
        self.build(elements)

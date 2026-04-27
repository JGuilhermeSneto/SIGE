import io
from datetime import datetime
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import qrcode

class InstitutionalPDF:
    """
    Classe base para geração de PDFs institucionais do SIGE usando ReportLab.
    Suporta cabeçalho dinâmico, rodapé com numeração e QR Code de autenticidade.
    """
    
    def __init__(self, buffer, title="Documento Oficial"):
        self.buffer = buffer
        self.title = title
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Configura estilos personalizados para o documento."""
        self.styles.add(ParagraphStyle(
            name='InstitutionalTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor("#1e3a8a"),  # Azul Corporativo SIGE
            alignment=1,  # Centralizado
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='LabelStyle',
            fontSize=9,
            textColor=colors.grey,
            textTransform='uppercase',
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='ValueStyle',
            fontSize=11,
            textColor=colors.black,
            fontName='Helvetica'
        ))

    def _draw_header_footer(self, canvas, doc):
        """Desenha o cabeçalho e rodapé em cada página."""
        canvas.saveState()
        
        # --- Cabeçalho ---
        canvas.setStrokeColor(colors.HexColor("#1e3a8a"))
        canvas.setLineWidth(2)
        canvas.line(1.5*cm, A4[1]-2.5*cm, A4[0]-1.5*cm, A4[1]-2.5*cm)
        
        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawCentredString(A4[0]/2, A4[1]-2.0*cm, "SIGE - Sistema Integrado de Gestão Escolar")
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2, A4[1]-2.35*cm, "Portal da Educação de Alta Performance")
        
        # --- Rodapé ---
        canvas.line(1.5*cm, 2*cm, A4[0]-1.5*cm, 2*cm)
        
        # Numeração de página
        page_num = canvas.getPageNumber()
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(A4[0]-1.5*cm, 1.5*cm, f"Página {page_num}")
        
        # Data e Hora de Emissão
        data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M")
        canvas.drawString(1.5*cm, 1.5*cm, f"Emitido em: {data_emissao}")
        
        # QR Code de Autenticidade (Placeholder)
        self._draw_qr_code(canvas)
        
        canvas.restoreState()

    def _draw_qr_code(self, canvas):
        """Gera e desenha um QR Code de autenticidade no rodapé."""
        # URL de verificação fictícia (será integrada com o módulo de validação depois)
        qr_data = f"https://sige.edu.br/validar/DOC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # Converte imagem para buffer compatível com ReportLab
        qr_buffer = io.BytesIO()
        img_qr.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        # Desenha no canvas
        canvas.drawImage(ImageReader(qr_buffer), A4[0]/2 - 0.7*cm, 0.8*cm, width=1.4*cm, height=1.4*cm)
        canvas.setFont('Helvetica-Bold', 6)
        canvas.drawCentredString(A4[0]/2, 0.6*cm, "VERIFICAR AUTENTICIDADE")

    def build(self, elements):
        """Constrói o PDF final."""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=3*cm,
            bottomMargin=3*cm,
            title=self.title
        )
        
        doc.build(elements, onFirstPage=self._draw_header_footer, onLaterPages=self._draw_header_footer)

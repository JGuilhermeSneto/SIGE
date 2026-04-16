import io
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors

class RelatorioMasterPDF:
    """Motor de Geração de PDFs Corporativos para o Módulo de BI com Marca D'água Dinâmica."""

    def __init__(self, titulo_relatorio="Relatório Oficial"):
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.titulo = titulo_relatorio

    def desenhar_marca_dagua(self, texto="CONFIDENCIAL - SIGE"):
        """Desenha uma marca d'água transversal por toda a página A4."""
        self.canvas.saveState()
        self.canvas.setFont("Helvetica-Bold", 60)
        self.canvas.setFillColor(colors.lightgrey, alpha=0.15)
        
        # Centraliza a rotação geométrica
        self.canvas.translate(self.width / 2, self.height / 2)
        self.canvas.rotate(45)
        self.canvas.drawCentredString(0, 0, texto)
        self.canvas.restoreState()

    def desenhar_cabecalho(self):
        """Cabeçalho Padrão do SIGE."""
        self.canvas.setFillColorRGB(0.04, 0.05, 0.1) # Cor Índigo Escuro Simulada
        self.canvas.rect(0, self.height - 2*cm, self.width, 2*cm, fill=1, stroke=0)
        
        self.canvas.setFillColor(colors.white)
        self.canvas.setFont("Helvetica-Bold", 14)
        self.canvas.drawString(1*cm, self.height - 1.2*cm, f"S.I.G.E | {self.titulo}")
        
        self.canvas.setFont("Helvetica", 10)
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.canvas.drawRightString(self.width - 1*cm, self.height - 1.2*cm, f"Gerado em: {data_hora}")

    def desenhar_bloco_estatistica(self, x, y, titulo, valor, alerta=False):
        """Plota um 'Card' de estatística bruto na página PDF."""
        self.canvas.setFillColor(colors.whitesmoke)
        self.canvas.roundRect(x, y, 5*cm, 2*cm, 4, fill=1, stroke=1)
        
        # Cor do Título
        self.canvas.setFillColor(colors.darkgrey)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x + 0.3*cm, y + 1.4*cm, titulo.upper())
        
        # Valor
        if alerta:
            self.canvas.setFillColorRGB(0.85, 0.1, 0.1) # Vermelho
        else:
            self.canvas.setFillColorRGB(0.1, 0.1, 0.2) # Default Texto
            
        self.canvas.setFont("Helvetica-Bold", 18)
        self.canvas.drawString(x + 0.3*cm, y + 0.5*cm, str(valor))

    def adicionar_tabela_evasao(self, eixo_y, dataset_alunos):
        """Plota a lista crítica formatada na folha."""
        self.canvas.setFont("Helvetica-Bold", 12)
        self.canvas.setFillColor(colors.black)
        self.canvas.drawString(1*cm, eixo_y, "LISTA CRÍTICA (Frequência < 75% ou Média < 5.0)")
        
        eixo_y -= 1*cm
        
        # Header Tabela
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.setFillColor(colors.white)
        self.canvas.rect(1*cm, eixo_y, self.width - 2*cm, 0.8*cm, fill=1, stroke=0)
        self.canvas.drawString(1.2*cm, eixo_y + 0.25*cm, "ALUNO")
        self.canvas.drawString(8.0*cm, eixo_y + 0.25*cm, "TURMA")
        self.canvas.drawString(12.0*cm, eixo_y + 0.25*cm, "TAXA FREQ.")
        self.canvas.drawString(16.0*cm, eixo_y + 0.25*cm, "MÉDIA")
        
        eixo_y -= 0.8*cm
        
        self.canvas.setFont("Helvetica", 9)
        self.canvas.setFillColor(colors.darkslategray)
        
        for aluno in dataset_alunos[:20]: # Protege para renderizar no max 20 pra caber 1 pag no doc base
            freq = f"{aluno.taxa_freq:.2f}%" if aluno.taxa_freq else "N/A"
            media = f"{aluno.avg_nota:.2f}" if aluno.avg_nota else "N/A"
            
            self.canvas.drawString(1.2*cm, eixo_y + 0.25*cm, aluno.nome_completo[:25] + '...')
            self.canvas.drawString(8.0*cm, eixo_y + 0.25*cm, str(aluno.turma.nome)[:15])
            
            # Highlight Preditivo
            if aluno.taxa_freq and aluno.taxa_freq < 75:
                self.canvas.setFillColorRGB(0.85, 0.1, 0.1)
                self.canvas.drawString(12.0*cm, eixo_y + 0.25*cm, freq)
                self.canvas.setFillColor(colors.darkslategray)
            else:
                self.canvas.drawString(12.0*cm, eixo_y + 0.25*cm, freq)
                
            self.canvas.drawString(16.0*cm, eixo_y + 0.25*cm, media)
            
            # Linha demarcatória
            self.canvas.setStrokeColor(colors.lightgrey)
            self.canvas.line(1*cm, eixo_y, self.width - 1*cm, eixo_y)
            
            eixo_y -= 0.8*cm
            
            # Evita Crash de Overpage simplista
            if eixo_y < 2*cm:
                self.canvas.showPage()
                self.desenhar_marca_dagua()
                self.desenhar_cabecalho()
                eixo_y = self.height - 4*cm

    def gerar_pdf(self, metricas):
        """Ponto de Entrada: Coordena todos os desenhos baseados no Dict de Métricas e emite o Buffer."""
        self.desenhar_marca_dagua()
        self.desenhar_cabecalho()
        
        # Plota os Cards Superiores
        y_cards = self.height - 4.5*cm
        self.desenhar_bloco_estatistica(1*cm, y_cards, "Geral (Alunos)", metricas['total_alunos'])
        self.desenhar_bloco_estatistica(6.5*cm, y_cards, "Em Risco Critico", metricas['total_risco'], alerta=True)
        self.desenhar_bloco_estatistica(12*cm, y_cards, "Livros Emprestados", metricas['livros_ativos'])
        
        # Plota a Tabela
        self.adicionar_tabela_evasao(y_cards - 2*cm, metricas['lista_evasao'])
        
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer

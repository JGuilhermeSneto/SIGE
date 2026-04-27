from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from .pdf_generator import InstitutionalPDF

class BoletimGenerator(InstitutionalPDF):
    """
    Gerador especializado para o Boletim Escolar.
    """
    
    def __init__(self, buffer, aluno, dados_boletim):
        super().__init__(buffer, title=f"Boletim_{aluno.nome_completo}")
        self.aluno = aluno
        self.dados = dados_boletim

    def generate(self):
        elements = []
        
        # Título do Documento
        elements.append(Paragraph("BOLETIM DE DESEMPENHO ESCOLAR", self.styles['InstitutionalTitle']))
        elements.append(Spacer(1, 0.5 * 10))
        
        # Informações do Aluno (Tabela Layout)
        info_data = [
            [Paragraph("ALUNO", self.styles['LabelStyle']), Paragraph("TURMA", self.styles['LabelStyle'])],
            [Paragraph(self.aluno.nome_completo.upper(), self.styles['ValueStyle']), Paragraph(self.aluno.turma.nome, self.styles['ValueStyle'])],
            [Paragraph("CPF", self.styles['LabelStyle']), Paragraph("ANO LETIVO", self.styles['LabelStyle'])],
            [Paragraph(self.aluno.cpf, self.styles['ValueStyle']), Paragraph(str(self.aluno.turma.ano), self.styles['ValueStyle'])]
        ]
        
        info_table = Table(info_data, colWidths=[10*10, 8*10]) # cm to points approximately or just use widths
        # Better use explicit cm
        from reportlab.lib.units import cm
        info_table = Table(info_data, colWidths=[11*cm, 7*cm])
        
        info_table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Tabela de Notas
        header = ["Disciplina", "1º B", "2º B", "3º B", "4º B", "Média", "Faltas", "% Freq"]
        table_data = [header]
        
        for item in self.dados:
            nota = item['nota']
            # Tratamento de valores nulos
            n1 = str(nota.nota1) if nota and nota.nota1 is not None else "--"
            n2 = str(nota.nota2) if nota and nota.nota2 is not None else "--"
            n3 = str(nota.nota3) if nota and nota.nota3 is not None else "--"
            n4 = str(nota.nota4) if nota and nota.nota4 is not None else "--"
            media = str(round(float(nota.media), 1)) if nota and nota.media is not None else "--"
            
            row = [
                item['disciplina'].nome,
                n1, n2, n3, n4,
                media,
                str(item['faltas']),
                f"{item['percentual_faltas']}%"
            ]
            table_data.append(row)
            
        # Estilo da Tabela de Notas
        notas_table = Table(table_data, colWidths=[6*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 2*cm, 2*cm, 2*cm])
        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'), # Disciplina à esquerda
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ])
        
        # Colorir médias reprovadas (Simulação de lógica premium)
        for i, item in enumerate(self.dados):
            media_val = float(item['nota'].media) if item['nota'] and item['nota'].media is not None else 0
            if media_val < 7.0:
                style.add('TEXTCOLOR', (5, i+1), (5, i+1), colors.HexColor("#dc2626")) # Vermelho
            else:
                style.add('TEXTCOLOR', (5, i+1), (5, i+1), colors.HexColor("#16a34a")) # Verde
                
        notas_table.setStyle(style)
        elements.append(notas_table)
        
        # Espaço para Assinaturas
        elements.append(Spacer(1, 40))
        
        signature_data = [
            ["____________________________________", "____________________________________"],
            ["Direção Escolar", "Secretaria Acadêmica"]
        ]
        sig_table = Table(signature_data, colWidths=[9*cm, 9*cm])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        elements.append(sig_table)
        
        # Constrói o PDF
        self.build(elements)

"""
Modelos de entidades acadêmicas: turma, disciplina, grade, atividades.

O que é: núcleo do domínio escolar; relaciona-se com ``usuarios.Professor``/``Aluno``
e com modelos de desempenho em ``desempenho.py``.
"""

from django.db import models
from django.utils import timezone
from apps.comum.models.modelo_base import TURNO_CHOICES

class Turma(models.Model):
    """Representa uma turma escolar."""
    nome = models.CharField(max_length=100, help_text="Nome da turma")
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES, help_text="Turno da turma")
    ano = models.IntegerField(help_text="Ano da turma")

    class Meta:
        db_table = 'core_turma'
        ordering = ["nome"]
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} - {self.get_turno_display()} ({self.ano})"


class Disciplina(models.Model):
    """Representa uma disciplina."""
    nome = models.CharField(max_length=100, help_text="Nome da disciplina")
    professor = models.ForeignKey(
        "usuarios.Professor", on_delete=models.CASCADE, related_name="disciplinas", help_text="Professor responsável"
    )
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, related_name="disciplinas", help_text="Turma associada"
    )

    class Meta:
        db_table = 'core_disciplina'
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return f"{self.nome} - {self.turma.nome}"


class GradeHorario(models.Model):
    """Representa a grade horária de uma turma."""
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="grades")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="grades")

    DIA_CHOICES = [
        ("segunda", "Segunda-feira"), ("terca", "Terça-feira"), ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"), ("sexta", "Sexta-feira"),
    ]
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    horario = models.CharField(max_length=20, help_text="Ex: 07:00 - 07:50")

    class Meta:
        db_table = 'core_gradehorario'
        verbose_name = "Grade de Horário"
        verbose_name_plural = "Grades de Horários"
        unique_together = ("turma", "dia", "horario")
        ordering = ["horario", "dia"]

    def __str__(self):
        return f"{self.turma} | {self.dia} | {self.horario} | {self.disciplina}"

class AtividadeProfessor(models.Model):
    """Representa um trabalho, atividade ou prova cadastrado pelo professor."""
    TIPO_CHOICES = [
        ('TRABALHO', 'Trabalho'),
        ('ATIVIDADE', 'Atividade'),
        ('PROVA', 'Prova'),
    ]
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="atividades", help_text="Disciplina associada")
    titulo = models.CharField(max_length=150, help_text="Título da Atividade/Prova")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='TRABALHO')
    data = models.DateField(help_text="Data do agendamento (para provas, deve coincidir com o calendário)")
    prazo_final = models.DateTimeField(null=True, blank=True, help_text="Data e Hora limite para entrega (Obrigatório para Atividade/Trabalho)")
    descricao = models.TextField(blank=True, help_text="Descrição detalhada")
    gabarito_liberado = models.BooleanField(
        default=False,
        help_text="Permite liberar gabarito manualmente antes do prazo.",
    )
    gabarito_liberado_em = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data/hora da liberação manual do gabarito.",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_atividadeprofessor'
        verbose_name = "Atividade de Professor"
        verbose_name_plural = "Atividades de Professores"
        ordering = ["-data", "titulo"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} - {self.data}"

    @property
    def prazo_encerrado(self):
        agora = timezone.localtime(timezone.now())
        if self.prazo_final:
            return agora > self.prazo_final
        if self.tipo == 'PROVA':
            return agora.date() > self.data
        return False

    @property
    def possui_gabarito(self):
        return self.questoes.exists()

    @property
    def exibir_gabarito_para_aluno(self):
        return self.possui_gabarito and (self.gabarito_liberado or self.prazo_encerrado)

class Questao(models.Model):
    """Questões de uma atividade (objetivas ou discursivas)."""
    TIPO_QUESTAO = [('OBJETIVA', 'Objetiva (Múltipla Escolha)'), ('DISCURSIVA', 'Discursiva (Texto)')]
    atividade = models.ForeignKey(AtividadeProfessor, on_delete=models.CASCADE, related_name="questoes")
    texto = models.TextField(help_text="Enunciado da questão")
    tipo = models.CharField(max_length=20, choices=TIPO_QUESTAO, default='OBJETIVA')
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, help_text="Valor em pontos desta questão")
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'core_questao'
        ordering = ['ordem']
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

class Alternativa(models.Model):
    """Opções para questões objetivas."""
    class Meta:
        db_table = 'core_alternativa'
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="alternativas")
    texto = models.CharField(max_length=255)
    eh_correta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correta' if self.eh_correta else 'Errada'})"

class EntregaAtividade(models.Model):
    """Armazena as entregas feitas pelos alunos."""
    STATUS_CHOICES = [('ENTREGUE', 'Entregue'), ('CORRIGIDO', 'Corrigido'), ('DEVOLVIDO', 'Devolvido')]
    aluno = models.ForeignKey("usuarios.Aluno", on_delete=models.CASCADE, related_name="entregas")
    atividade = models.ForeignKey(AtividadeProfessor, on_delete=models.CASCADE, related_name="entregas")
    arquivo = models.FileField(upload_to="entregas/atividades/", blank=True, null=True)
    comentario_aluno = models.TextField(blank=True)
    feedback_professor = models.TextField(blank=True, help_text="Feedback geral da correção")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENTREGUE')
    data_entrega = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_entregaatividade'
        unique_together = ("aluno", "atividade")
        ordering = ["-data_entrega"]

class RespostaAluno(models.Model):
    """Respostas individuais de cada questão."""
    class Meta:
        db_table = 'core_respostaaluno'
    entrega = models.ForeignKey(EntregaAtividade, on_delete=models.CASCADE, related_name="respostas")
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa_escolhida = models.ForeignKey(Alternativa, on_delete=models.SET_NULL, null=True, blank=True)
    texto_resposta = models.TextField(blank=True, null=True, help_text="Para questões discursivas")
    comentario_professor = models.TextField(blank=True, help_text="Correção específica desta questão")
    pontos_atribuidos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class PlanejamentoAula(models.Model):
    """Diário de classe onde o professor registra o plano/conteúdo que vai ou que foi ministrado via Grade Horária."""
    professor = models.ForeignKey("usuarios.Professor", on_delete=models.CASCADE, related_name="planejamentos_aula")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="planejamentos_aula")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="planejamentos_aula")
    data_aula = models.DateField(help_text="Data efetiva da aula")
    horario_aula = models.CharField(max_length=50, help_text="Horário conforme a Grade (Ex: 07:00 - 07:50)")
    
    conteudo = models.TextField(help_text="Descrição do plano de aula ou conteúdo abordado (Markdown opcional)")
    arquivos_apoio = models.FileField(upload_to="planejamentos/materiais/", blank=True, null=True, help_text="Upload de lista de exercícios ou slides da aula")
    
    STATUS_AULA_CHOICES = [
        ('NORMAL', 'Normal'),
        ('SUSPENSA', 'Suspensa'),
        ('CANCELADA', 'Cancelada'),
    ]

    status = models.CharField(max_length=15, choices=STATUS_AULA_CHOICES, default='NORMAL')
    concluido = models.BooleanField(default=False, help_text="Se verificado como True, a aula já foi dada e consumida.")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_planejamentoaula'
        unique_together = ("disciplina", "data_aula", "horario_aula")
        ordering = ["-data_aula", "horario_aula"]
        verbose_name = "Planejamento de Aula"
        verbose_name_plural = "Planejamentos de Aulas"

    def __str__(self):
        return f"{self.data_aula.strftime('%d/%m/%Y')} | {self.disciplina.nome} | {self.horario_aula}"

class MaterialDidatico(models.Model):
    """Representa um material de aula (link, arquivo ou livro da biblioteca)."""
    TIPO_CHOICES = [
        ('LINK', 'Link Externo'),
        ('ARQUIVO', 'Arquivo de Apoio'),
        ('LIVRO', 'Livro da Biblioteca'),
    ]
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="materiais")
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='LINK')
    
    # Para LINK
    url = models.URLField(blank=True, null=True, help_text="Link externo (YouTube, site, etc.)")
    
    # Para ARQUIVO
    arquivo = models.FileField(upload_to='materiais_aula/', blank=True, null=True)
    
    # Para LIVRO
    livro = models.ForeignKey(
        'biblioteca.Livro', on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Referência a um livro do acervo"
    )
    
    descricao = models.TextField(blank=True, help_text="Descrição ou instruções do professor")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_materialdidatico'
        verbose_name = "Material Didático"
        verbose_name_plural = "Materiais Didáticos"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

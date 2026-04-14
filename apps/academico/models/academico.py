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
        return self.possui_gabarito and self.prazo_encerrado

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

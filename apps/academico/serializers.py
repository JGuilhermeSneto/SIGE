from rest_framework import serializers
from .models import (
    Turma, Disciplina, GradeHorario, AtividadeProfessor, Questao, Alternativa, MaterialDidatico,
    Frequencia, Nota, NotaAtividade, Notificacao
)
from apps.usuarios.models import Professor, Aluno


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "nome", "turno", "ano"]


class DisciplinaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.ReadOnlyField(source="professor.nome_completo")
    turma_nome = serializers.ReadOnlyField(source="turma.nome")

    class Meta:
        model = Disciplina
        fields = ["id", "nome", "professor", "professor_nome", "turma", "turma_nome"]


class GradeHorarioSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.ReadOnlyField(source="disciplina.nome")
    dia_display = serializers.CharField(source="get_dia_display", read_only=True)

    class Meta:
        model = GradeHorario
        fields = ["id", "turma", "disciplina", "disciplina_nome", "dia", "dia_display", "horario"]


class AtividadeProfessorSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    disciplina_nome = serializers.ReadOnlyField(source="disciplina.nome")

    class Meta:
        model = AtividadeProfessor
        fields = [
            "id",
            "disciplina",
            "disciplina_nome",
            "titulo",
            "tipo",
            "tipo_display",
            "data",
            "prazo_final",
            "descricao",
            "gabarito_liberado",
            "criado_em",
        ]


class FrequenciaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.ReadOnlyField(source="aluno.nome_completo")
    disciplina_nome = serializers.ReadOnlyField(source="disciplina.nome")

    class Meta:
        model = Frequencia
        fields = [
            "id",
            "aluno",
            "aluno_nome",
            "disciplina",
            "disciplina_nome",
            "data",
            "presente",
            "justificada",
            "observacao",
        ]


class NotaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.ReadOnlyField(source="aluno.nome_completo")
    disciplina_nome = serializers.ReadOnlyField(source="disciplina.nome")
    media = serializers.ReadOnlyField()

    class Meta:
        model = Nota
        fields = [
            "id",
            "aluno",
            "aluno_nome",
            "disciplina",
            "disciplina_nome",
            "nota1",
            "nota2",
            "nota3",
            "nota4",
            "media",
            "observacao",
        ]


class MaterialDidaticoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    disciplina_nome = serializers.ReadOnlyField(source="disciplina.nome")

    class Meta:
        model = MaterialDidatico
        fields = [
            "id",
            "disciplina",
            "disciplina_nome",
            "titulo",
            "tipo",
            "tipo_display",
            "url",
            "arquivo",
            "livro",
            "descricao",
            "criado_em",
        ]


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = [
            "id",
            "tipo",
            "titulo",
            "mensagem",
            "url_destino",
            "lida",
            "criado_em",
        ]

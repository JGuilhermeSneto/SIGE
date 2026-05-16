from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Turma, Disciplina, GradeHorario, AtividadeProfessor, MaterialDidatico,
    Frequencia, Nota, Notificacao
)
from .serializers import (
    TurmaSerializer,
    DisciplinaSerializer,
    GradeHorarioSerializer,
    AtividadeProfessorSerializer,
    FrequenciaSerializer,
    NotaSerializer,
    MaterialDidaticoSerializer,
    NotificacaoSerializer,
)


class TurmaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para visualização de turmas.
    Gestores veem tudo, professores veem suas turmas, alunos veem a sua.
    """
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "gestor"):
            return Turma.objects.filter(instituicao=user.gestor.instituicao)
        if hasattr(user, "professor"):
            return Turma.objects.filter(disciplinas__professor=user.professor).distinct()
        if hasattr(user, "aluno"):
            return Turma.objects.filter(id=user.aluno.turma_id)
        return Turma.objects.none()


class DisciplinaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para visualização de disciplinas.
    Professores veem as que lecionam, alunos veem as de sua turma.
    """
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "gestor"):
            return Disciplina.objects.filter(turma__instituicao=user.gestor.instituicao)
        if hasattr(user, "professor"):
            return Disciplina.objects.filter(professor=user.professor)
        if hasattr(user, "aluno"):
            return Disciplina.objects.filter(turma=user.aluno.turma)
        return Disciplina.objects.none()


class GradeHorarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para visualização da grade horária.
    """
    serializer_class = GradeHorarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "gestor"):
            return GradeHorario.objects.filter(turma__instituicao=user.gestor.instituicao)
        if hasattr(user, "professor"):
            return GradeHorario.objects.filter(disciplina__professor=user.professor)
        if hasattr(user, "aluno"):
            return GradeHorario.objects.filter(turma=user.aluno.turma)
        return GradeHorario.objects.none()


class AtividadeProfessorViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar atividades e provas.
    """
    serializer_class = AtividadeProfessorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "professor"):
            return AtividadeProfessor.objects.filter(disciplina__professor=user.professor)
        if hasattr(user, "aluno"):
            return AtividadeProfessor.objects.filter(disciplina__turma=user.aluno.turma)
        return AtividadeProfessor.objects.none()


class FrequenciaViewSet(viewsets.ModelViewSet):
    """
    API para registro e consulta de frequência.
    """
    serializer_class = FrequenciaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "professor"):
            return Frequencia.objects.filter(disciplina__professor=user.professor)
        if hasattr(user, "aluno"):
            return Frequencia.objects.filter(aluno=user.aluno)
        return Frequencia.objects.none()


class NotaViewSet(viewsets.ModelViewSet):
    """
    API para lançamento e consulta de notas.
    """
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "professor"):
            return Nota.objects.filter(disciplina__professor=user.professor)
        if hasattr(user, "aluno"):
            return Nota.objects.filter(aluno=user.aluno)
        return Nota.objects.none()


class MaterialDidaticoViewSet(viewsets.ModelViewSet):
    """
    API para materiais didáticos.
    """
    serializer_class = MaterialDidaticoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "professor"):
            return MaterialDidatico.objects.filter(disciplina__professor=user.professor)
        if hasattr(user, "aluno"):
            return MaterialDidatico.objects.filter(disciplina__turma=user.aluno.turma)
        return MaterialDidatico.objects.none()


class NotificacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para listar e gerenciar notificações do usuário autenticado.
    Acesso universal: Qualquer usuário autenticado vê suas próprias notificações.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user).order_by("-criado_em")

    @action(detail=True, methods=["post"])
    def marcar_lida(self, request, pk=None):
        notificacao = self.get_object()
        notificacao.lida = True
        notificacao.save()
        return Response({"status": "notificação marcada como lida", "lida": True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def marcar_todas_lidas(self, request):
        Notificacao.objects.filter(usuario=self.request.user, lida=False).update(lida=True)
        return Response({"status": "todas notificações marcadas como lidas"}, status=status.HTTP_200_OK)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

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


from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q
from apps.academico.selectors.desempenho_selectors import DesempenhoSelector
from apps.academico.utils.academico import _get_grade_horario_turma, _calcular_situacao_nota
from apps.comunicacao.models import Comunicado
from apps.biblioteca.models.biblioteca import Emprestimo
from apps.academico.models import GradeHorario

class AlunoDashboardView(APIView):
    """
    API endpoint para o dashboard consolidado do aluno logado.
    Exibe: resumo acadêmico (média geral, faltas, situação), controle parental,
    grade horária de hoje, comunicados ativos (mural), livros em posse e desempenho gráfico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response(
                {"detail": "Usuário não possui perfil de aluno."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 1. Resumo Acadêmico
        disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
        soma_medias = 0
        total_disciplinas_com_media = 0
        total_aulas_gerais = 0
        faltas_gerais = 0

        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            if nota and nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1
            
            freqs = d.frequencias_aluno_prefetched
            total_aulas_gerais += len(freqs)
            faltas_gerais += len([f for f in freqs if not f.presente])

        media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0.0
        percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)

        if total_disciplinas_com_media > 0 or total_aulas_gerais > 0:
            sit_dict = _calcular_situacao_nota(media_geral, percentual_frequencia_geral)
            situacao_geral = sit_dict["texto"]
        else:
            situacao_geral = "Sem dados"

        # 2. Controle Parental
        parental_ativo = False
        responsavel = aluno.responsaveis.filter(controle_parental_ativo=True).first()
        if responsavel:
            parental_ativo = True

        # 3. Grade Horária de Hoje
        hoje_date = timezone.now().date()
        dia_semana_map = {
            0: "SEG",
            1: "TER",
            2: "QUA",
            3: "QUI",
            4: "SEX",
            5: "SAB",
            6: "DOM"
        }
        dia_semana_sigla = dia_semana_map[hoje_date.weekday()]
        
        grade_hoje = GradeHorario.objects.filter(turma=aluno.turma, dia=dia_semana_sigla).order_by("horario")
        grade_list = []
        for item in grade_hoje:
            grade_list.append({
                "id": item.id,
                "horario": item.horario,
                "disciplina": item.disciplina.nome if item.disciplina else "Intervalo"
            })

        # 4. Mural de Avisos (Comunicados)
        hoje = timezone.now().date()
        comunicados = Comunicado.objects.filter(
            Q(publico_alvo__in=["GLOBAL", "ALUNOS"]),
            Q(data_expiracao__isnull=True) | Q(data_expiracao__gte=hoje)
        ).order_by("-data_publicacao")[:5]

        mural_list = []
        for c in comunicados:
            mural_list.append({
                "id": c.id,
                "titulo": c.titulo,
                "conteudo": c.conteudo,
                "data_publicacao": c.data_publicacao,
                "importancia": c.importancia
            })

        # 5. Livros em Posse
        emprestimos = (
            Emprestimo.objects.filter(usuario_aluno=aluno)
            .exclude(status="DEVOLVIDO")
            .select_related("livro")
            .order_by("-data_emprestimo")
        )
        livros_list = []
        for emp in emprestimos:
            livros_list.append({
                "id": emp.id,
                "titulo": emp.livro.titulo,
                "autor": emp.livro.autor,
                "status": emp.status,
                "atrasado": emp.status == "ATRASADO"
            })

        # 6. Desempenho Gráfico
        desempenho_grafico = []
        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            media = float(nota.media) if (nota and nota.media is not None) else 0.0
            desempenho_grafico.append({
                "disciplina": d.nome[:3].upper(),
                "media": media
            })

        # Monta grade da semana inteira para o seletor de dias do mobile
        dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]
        grade_semana = {}
        for dia in dias_semana:
            items = GradeHorario.objects.filter(turma=aluno.turma, dia=dia).order_by("horario")
            grade_semana[dia] = [
                {
                    "id": item.id,
                    "horario": item.horario,
                    "disciplina": item.disciplina.nome if item.disciplina else "Intervalo"
                }
                for item in items
            ]

        # Obter a foto de perfil (ou avatar placeholder)
        foto_url = aluno.get_foto_url
        if foto_url and not foto_url.startswith(("http://", "https://")):
            foto_url = request.build_absolute_uri(foto_url)

        return Response({
            "aluno": {
                "id": aluno.id,
                "nome_completo": aluno.nome_completo,
                "turma": aluno.turma.nome if aluno.turma else "Sem Turma",
                "turno": aluno.turma.get_turno_display() if aluno.turma else "Sem Turno",
                "ano_letivo": aluno.turma.ano if aluno.turma else "",
                "foto_url": foto_url
            },
            "parental_control": {
                "ativo": parental_ativo
            },
            "summary": {
                "disciplinas": disciplinas.count(),
                "media_geral": round(media_geral, 1),
                "situacao": situacao_geral,
                "faltas_detalhe": f"{faltas_gerais}/{total_aulas_gerais if total_aulas_gerais > 0 else 100}",
                "faltas": faltas_gerais,
                "frequencia_total": round(percentual_frequencia_geral, 1)
            },
            "mural": mural_list,
            "grade_hoje": grade_list,
            "grade_semana": grade_semana,
            "livros_posse": livros_list,
            "desempenho_grafico": desempenho_grafico
        }, status=status.HTTP_200_OK)


class AlunoBoletimView(APIView):
    """
    API endpoint para o boletim acadêmico do aluno.
    Exibe: notas bimestrais, médias, faltas, frequência por disciplina e materiais recentes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response(
                {"detail": "Usuário não possui perfil de aluno."},
                status=status.HTTP_403_FORBIDDEN
            )

        disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
        boletim_list = []
        soma_medias = 0
        total_disciplinas_com_media = 0
        total_aulas_gerais = 0
        faltas_gerais = 0

        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            frequencias = d.frequencias_aluno_prefetched
            total_aulas = len(frequencias)
            faltas = len([f for f in frequencias if not f.presente])
            presencas = total_aulas - faltas
            percentual_presenca = (presencas / total_aulas * 100) if total_aulas > 0 else 100.0

            total_aulas_gerais += total_aulas
            faltas_gerais += faltas

            media = float(nota.media) if (nota and nota.media is not None) else None
            if media is not None:
                soma_medias += media
                total_disciplinas_com_media += 1

            if media is not None:
                if media >= 7.0 and percentual_presenca >= 75:
                    status_disc = "aprovado"
                elif media >= 5.0 and percentual_presenca >= 75:
                    status_disc = "recuperacao"
                else:
                    status_disc = "reprovado"
            else:
                status_disc = "aprovado"

            # Materiais didáticos recentes para esta disciplina
            from apps.academico.models import MaterialDidatico
            materiais = MaterialDidatico.objects.filter(disciplina=d).order_by("-criado_em")[:3]
            materiais_list = []
            for mat in materiais:
                materiais_list.append(mat.titulo)

            boletim_list.append({
                "id": d.id,
                "nome": d.nome.upper(),
                "prof": d.professor.nome_completo if d.professor else "Sem Professor",
                "media": str(round(media, 1)) if media is not None else "--",
                "status": status_disc,
                "notas": {
                    "b1": str(round(nota.nota1, 1)) if (nota and nota.nota1 is not None) else "--",
                    "b2": str(round(nota.nota2, 1)) if (nota and nota.nota2 is not None) else "--",
                    "b3": str(round(nota.nota3, 1)) if (nota and nota.nota3 is not None) else "--",
                    "b4": str(round(nota.nota4, 1)) if (nota and nota.nota4 is not None) else "--"
                },
                "faltas": faltas,
                "total": total_aulas if total_aulas > 0 else 40,
                "freq": int(percentual_presenca),
                "materiais": materiais_list
            })

        media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0.0
        percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)

        return Response({
            "media_geral": round(media_geral, 1),
            "frequencia_total": int(percentual_frequencia_geral),
            "boletim": boletim_list
        }, status=status.HTTP_200_OK)


class AlunoPerfilView(APIView):
    """
    API endpoint para visualizar e atualizar o perfil do aluno logado.
    GET: Retorna dados pessoais, acadêmicos, responsáveis e estatísticas.
    PUT: Permite atualizar campos pessoais (nome, cpf, data_nascimento, naturalidade, telefone) e a foto de perfil.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response({"detail": "Usuário não possui perfil de aluno."}, status=status.HTTP_403_FORBIDDEN)

        # Estatísticas consolidadas (reutiliza lógica do dashboard)
        disciplinas = DesempenhoSelector.get_resumo_academico_aluno(aluno)
        soma_medias = 0
        total_disc_com_media = 0
        total_aulas = 0
        total_faltas = 0

        for d in disciplinas:
            nota = d.nota_aluno_prefetched[0] if d.nota_aluno_prefetched else None
            freqs = d.frequencias_aluno_prefetched
            total_aulas += len(freqs)
            faltas = len([f for f in freqs if not f.presente])
            total_faltas += faltas
            if nota and nota.media is not None:
                soma_medias += float(nota.media)
                total_disc_com_media += 1

        media_geral = round(soma_medias / total_disc_com_media, 1) if total_disc_com_media > 0 else 0.0
        pct_freq = round(100 - ((total_faltas / total_aulas * 100) if total_aulas > 0 else 0), 1)

        # Dados do responsável
        responsaveis_list = []
        for resp in aluno.responsaveis.all():
            responsaveis_list.append({
                "nome": resp.nome_completo,
                "parentesco": resp.parentesco or "—",
                "telefone": resp.telefone or "—",
            })

        # Obter a foto de perfil (ou avatar placeholder)
        foto_url = aluno.get_foto_url
        if foto_url and not foto_url.startswith(("http://", "https://")):
            foto_url = request.build_absolute_uri(foto_url)

        return Response({
            "nome": aluno.nome_completo,
            "matricula": aluno.matricula or "—",
            "cpf": aluno.cpf or "—",
            "data_nascimento": aluno.data_nascimento.strftime("%d/%m/%Y") if aluno.data_nascimento else "",
            "naturalidade": aluno.naturalidade or "",
            "telefone": aluno.telefone or "",
            "turma": aluno.turma.nome if aluno.turma else "—",
            "turno": aluno.turma.get_turno_display() if aluno.turma else "—",
            "ano_letivo": str(aluno.turma.ano) if aluno.turma else "—",
            "status_matricula": aluno.get_status_matricula_display(),
            "foto_url": foto_url,
            "stats": {
                "media_geral": str(media_geral),
                "frequencia": f"{pct_freq}%",
                "disciplinas": str(disciplinas.count()),
                "faltas": str(total_faltas),
            },
            "responsaveis": responsaveis_list,
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response({"detail": "Usuário não possui perfil de aluno."}, status=status.HTTP_403_FORBIDDEN)

        dados = request.data
        if "nome" in dados and dados["nome"].strip():
            aluno.nome_completo = dados["nome"].strip()
        if "naturalidade" in dados:
            aluno.naturalidade = dados["naturalidade"].strip()
        if "telefone" in dados:
            aluno.telefone = dados["telefone"].strip()
        if "cpf" in dados and dados["cpf"].strip():
            aluno.cpf = dados["cpf"].strip()
        if "data_nascimento" in dados and dados["data_nascimento"].strip():
            from datetime import datetime
            try:
                aluno.data_nascimento = datetime.strptime(dados["data_nascimento"].strip(), "%d/%m/%Y").date()
            except ValueError:
                pass

        # Atualizar ou remover foto de perfil
        foto = request.FILES.get("foto") or request.data.get("foto")
        if foto and not isinstance(foto, str):
            if aluno.foto:
                try:
                    aluno.foto.delete(save=False)
                except Exception:
                    pass
            aluno.foto = foto
        elif dados.get("remover_foto") == "true" or dados.get("remover_foto") is True:
            if aluno.foto:
                try:
                    aluno.foto.delete(save=False)
                except Exception:
                    pass
            aluno.foto = None

        aluno.save()

        foto_url = aluno.get_foto_url
        if foto_url and not foto_url.startswith(("http://", "https://")):
            foto_url = request.build_absolute_uri(foto_url)

        return Response({
            "detail": "Perfil atualizado com sucesso.",
            "foto_url": foto_url
        }, status=status.HTTP_200_OK)


class AlunoRoteiroView(APIView):
    """
    API endpoint para o roteiro (trilha educacional) do aluno.
    Retorna as disciplinas da turma e os planejamentos de aula de cada uma (PlanejamentoAula).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response({"detail": "Usuário não possui perfil de aluno."}, status=status.HTTP_403_FORBIDDEN)

        from apps.academico.models.academico import PlanejamentoAula
        import locale

        disciplinas = Disciplina.objects.filter(turma=aluno.turma).select_related("professor").order_by("nome")

        materias_list = []
        aulas_dict = {}

        dias_pt = {
            0: "Segunda-Feira",
            1: "Terça-Feira",
            2: "Quarta-Feira",
            3: "Quinta-Feira",
            4: "Sexta-Feira",
            5: "Sábado",
            6: "Domingo",
        }
        meses_pt = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }

        for d in disciplinas:
            materias_list.append({
                "id": d.id,
                "nome": d.nome,
                "professor": d.professor.nome_completo if d.professor else "Sem Professor",
            })

            planejamentos = PlanejamentoAula.objects.filter(
                disciplina=d, turma=aluno.turma
            ).order_by("-data_aula")

            aulas = []
            for p in planejamentos:
                nome_dia = dias_pt.get(p.data_aula.weekday(), "")
                dia_num = p.data_aula.day
                nome_mes = meses_pt.get(p.data_aula.month, "")
                ano = p.data_aula.year
                data_fmt = f"{nome_dia}, {dia_num:02d} De {nome_mes} De {ano}"
                situacao = "concluida" if p.concluido else "pendente"
                aulas.append({
                    "data": data_fmt,
                    "situacao": situacao,
                    "assunto": p.conteudo[:60] if p.conteudo else "Sem título",
                    "topicos": p.conteudo[60:120] if len(p.conteudo) > 60 else "",
                })

            aulas_dict[str(d.id)] = aulas

        return Response({
            "materias": materias_list,
            "aulas": aulas_dict,
        }, status=status.HTTP_200_OK)


class AlunoMateriaisView(APIView):
    """
    API endpoint para os materiais didáticos do aluno.
    Retorna os materiais organizados por disciplina, com tipo, URL e título.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        aluno = getattr(user, "aluno", None)
        if not aluno:
            return Response({"detail": "Usuário não possui perfil de aluno."}, status=status.HTTP_403_FORBIDDEN)

        disciplinas = Disciplina.objects.filter(turma=aluno.turma).select_related("professor").order_by("nome")

        resultado = []
        for d in disciplinas:
            materiais = MaterialDidatico.objects.filter(disciplina=d).order_by("-criado_em")
            arquivos = []
            for mat in materiais:
                if mat.tipo == "ARQUIVO" and mat.arquivo:
                    try:
                        url = request.build_absolute_uri(mat.arquivo.url)
                    except Exception:
                        url = None
                elif mat.tipo == "LINK":
                    url = mat.url
                else:
                    url = None

                arquivos.append({
                    "nome": mat.titulo,
                    "meta": f"{mat.get_tipo_display()} · {mat.descricao[:40] if mat.descricao else ''}",
                    "quantidade": 1,
                    "url": url,
                    "tipo": mat.tipo,
                })

            if arquivos:
                resultado.append({
                    "id": d.id,
                    "nome": d.nome,
                    "professor": d.professor.nome_completo if d.professor else "Sem Professor",
                    "arquivos": arquivos,
                })

        return Response(resultado, status=status.HTTP_200_OK)


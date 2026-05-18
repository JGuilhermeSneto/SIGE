from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from ...models.perfis import Professor
from ...forms.perfis import ProfessorForm
from ...utils.perfis import get_nome_exibicao, get_foto_perfil, is_super_ou_gestor
from apps.academico.services.notificacao_servico import NotificacaoServico
from django.core.exceptions import ValidationError
from .helpers import exibir_erros_formulario


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_professores(request):
    """Lista os professores cadastrados."""
    query = request.GET.get("q", "")
    professores = Professor.objects.all().select_related("user")
    if query:
        professores = professores.filter(nome_completo__icontains=query)
    return render(
        request,
        "professor/listar_professores.html",
        {
            "professores": professores,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_professor(request):
    """Novo professor e usuário."""
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            try:
                professor = form.save()
                NotificacaoServico.notificar_gestores(
                    tipo="SISTEMA",
                    titulo="Novo Professor Cadastrado",
                    mensagem=f"O professor {professor.nome_completo} foi integrado ao sistema.",
                    url_destino="/usuarios/professores/",
                )
                messages.success(
                    request,
                    f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
                )
                return redirect("listar_professores")
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
        else:
            exibir_erros_formulario(request, form)
    else:
        form = ProfessorForm(request=request)
    return render(
        request,
        "professor/cadastrar_professor.html",
        {
            "form": form,
            "professor": None,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_professor(request, professor_id):
    """Edita professor."""
    professor = get_object_or_404(Professor, id=professor_id)
    if request.method == "POST":
        form = ProfessorForm(
            request.POST, request.FILES, instance=professor, request=request
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    f"Professor(a) {professor.nome_completo} atualizado(a) com sucesso!",
                )
                return redirect("listar_professores")
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar: {str(e)}")
        else:
            exibir_erros_formulario(request, form)
    else:
        form = ProfessorForm(instance=professor, request=request)
    return render(
        request,
        "professor/cadastrar_professor.html",
        {
            "form": form,
            "professor": professor,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_professor(request, professor_id):
    """Remove professor."""
    professor = get_object_or_404(Professor, id=professor_id)
    try:
        nome = professor.nome_completo
        professor.user.delete()
        messages.success(request, f"Professor(a) {nome} removido(a) com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao remover professor: {str(e)}")
    return redirect("listar_professores")

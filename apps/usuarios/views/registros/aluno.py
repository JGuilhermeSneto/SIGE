from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from ...models.perfis import Aluno
from ...forms.perfis import AlunoForm
from apps.saude.forms import FichaMedicaForm
from ...utils.perfis import get_nome_exibicao, get_foto_perfil, is_super_ou_gestor
from apps.academico.services.notificacao_servico import NotificacaoServico
from django.core.exceptions import ValidationError
from .helpers import exibir_erros_cadastro_aluno


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_alunos(request):
    """Lista alunos."""
    query = request.GET.get("q", "")
    alunos = Aluno.objects.all().select_related("user", "turma", "ficha_medica")
    if query:
        alunos = alunos.filter(nome_completo__icontains=query)
    return render(
        request,
        "aluno/listar_alunos.html",
        {
            "alunos": alunos,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_aluno(request):
    """Matrícula aluno e cria ficha médica."""
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, request=request)
        form_saude = FichaMedicaForm(request.POST, request.FILES)

        if form.is_valid() and form_saude.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save()
                    ficha = form_saude.save(commit=False)
                    ficha.aluno = aluno
                    ficha.condicoes_pcd = aluno.possui_necessidade_especial
                    ficha.save()

                    NotificacaoServico.notificar_gestores(
                        tipo="SISTEMA",
                        titulo="Novo Aluno Matriculado",
                        mensagem=f"O aluno {aluno.nome_completo} foi matriculado na turma {aluno.turma.nome if aluno.turma else 'Sem Turma'}.",
                        url_destino="/usuarios/alunos/",
                    )
                    messages.success(
                        request,
                        f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!",
                    )
                    return redirect("listar_alunos")
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
        else:
            exibir_erros_cadastro_aluno(request, form, form_saude)
    else:
        form = AlunoForm(request=request)
        form_saude = FichaMedicaForm()

    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form": form,
            "form_saude": form_saude,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_aluno(request, aluno_id):
    """Edita prontuário e ficha médica."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ficha_medica = getattr(aluno, "ficha_medica", None)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno, request=request)
        form_saude = FichaMedicaForm(request.POST, request.FILES, instance=ficha_medica)

        if form.is_valid() and form_saude.is_valid():
            try:
                with transaction.atomic():
                    aluno_salvo = form.save()
                    ficha = form_saude.save(commit=False)
                    ficha.aluno = aluno_salvo
                    ficha.condicoes_pcd = aluno_salvo.possui_necessidade_especial
                    ficha.save()
                    messages.success(request, "Aluno e Ficha Médica atualizados!")
                    return redirect("listar_alunos")
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar: {str(e)}")
        else:
            exibir_erros_cadastro_aluno(request, form, form_saude)
    else:
        form = AlunoForm(instance=aluno, request=request)
        form_saude = FichaMedicaForm(instance=ficha_medica)

    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form": form,
            "form_saude": form_saude,
            "aluno": aluno,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_aluno(request, aluno_id):
    """Remove aluno."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    try:
        if aluno.user:
            aluno.user.delete()
        else:
            aluno.delete()
        messages.success(request, "Aluno removido.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect("listar_alunos")

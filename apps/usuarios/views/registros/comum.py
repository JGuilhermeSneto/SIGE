from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from ...models.perfis import Professor, Aluno, Gestor
from ...utils.perfis import get_nome_exibicao, get_foto_perfil, is_super_ou_gestor

@login_required
@user_passes_test(is_super_ou_gestor)
def usuarios(request):
    """Controla o acesso à listagem geral de usuários com estatisticas básicas."""
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_gestores = Gestor.objects.count()
    total_usuarios = total_alunos + total_professores + total_gestores
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    total_ativos = User.objects.filter(is_active=True).count()
    total_desativados = User.objects.filter(is_active=False).count()

    alunos_ativos = Aluno.objects.filter(user__is_active=True).count()
    alunos_inativos = Aluno.objects.filter(user__is_active=False).count()
    professores_ativos = Professor.objects.filter(user__is_active=True).count()
    professores_inativos = Professor.objects.filter(user__is_active=False).count()
    gestores_ativos = Gestor.objects.filter(user__is_active=True).count()
    gestores_inativos = Gestor.objects.filter(user__is_active=False).count()
    
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor") and request.user.gestor.cargo in ("diretor", "vice_diretor")
    )
    
    return render(request, "core/usuarios.html", {
        "pode_ver_gestores":     pode_ver_gestores,
        "total_alunos":          total_alunos,
        "total_professores":     total_professores,
        "total_gestores":        total_gestores,
        "total_usuarios":        total_usuarios,
        "total_ativos":          total_ativos,
        "total_desativados":     total_desativados,
        "alunos_ativos":        alunos_ativos,
        "alunos_inativos":      alunos_inativos,
        "professores_ativos":   professores_ativos,
        "professores_inativos": professores_inativos,
        "gestores_ativos":      gestores_ativos,
        "gestores_inativos":    gestores_inativos,
        "nome_exibicao":         get_nome_exibicao(request.user),
        "foto_perfil_url":       get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_desativados(request):
    """Exibe todos os usuários que estão com is_active=False."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    usuarios_inativos = User.objects.filter(is_active=False).order_by("-date_joined")
    return render(request, "core/listar_desativados.html", {
        "usuarios":        usuarios_inativos,
        "nome_exibicao":   get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def reativar_usuario(request, user_id):
    """Reativa um usuário desativado."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_to_activate = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user_to_activate.is_active = True
        user_to_activate.save()
        messages.success(request, f"Usuário {user_to_activate.username} reativado com sucesso!")
    return redirect("listar_desativados")

@login_required
@user_passes_test(is_super_ou_gestor)
def desativar_usuario(request, user_id):
    """Desativa um usuário (is_active=False)."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_to_deactivate = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        if user_to_deactivate == request.user:
            messages.error(request, "Você não pode desativar seu próprio acesso!")
        else:
            user_to_deactivate.is_active = False
            user_to_deactivate.save()
            messages.success(request, f"Usuário {user_to_deactivate.username} desativado com sucesso!")
        referer = request.META.get('HTTP_REFERER')
        if referer: return redirect(referer)
        return redirect("usuarios")
    return redirect("usuarios")

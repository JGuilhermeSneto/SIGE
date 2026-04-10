from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import datetime

from ..models import Professor, Aluno, Gestor, Turma
from ..forms import ProfessorForm, AlunoForm, GestorForm, TurmaForm
from ..utils import get_nome_exibicao, get_foto_perfil, _get_anos_filtro

# Permissão customizada para Superusuário ou Gestor
def is_super_ou_gestor(u):
    return u.is_superuser or hasattr(u, "gestor")

def is_superuser(u):
    return u.is_superuser

@login_required
@user_passes_test(is_super_ou_gestor)
def usuarios(request):
    """Controla o acesso à listagem geral de usuários com estatisticas básicas."""
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_gestores = Gestor.objects.count()
    
    # Busca o total de usuarios cadastrados nos perfis
    total_usuarios = total_alunos + total_professores + total_gestores
    
    # Busca o total de usuarios ativos no sistema
    from django.contrib.auth import get_user_model
    User = get_user_model()
    total_ativos = User.objects.filter(is_active=True).count()
    total_desativados = User.objects.filter(is_active=False).count()

    # Estatísticas por categoria
    alunos_ativos = Aluno.objects.filter(user__is_active=True).count()
    alunos_inativos = Aluno.objects.filter(user__is_active=False).count()
    
    professores_ativos = Professor.objects.filter(user__is_active=True).count()
    professores_inativos = Professor.objects.filter(user__is_active=False).count()
    
    gestores_ativos = Gestor.objects.filter(user__is_active=True).count()
    gestores_inativos = Gestor.objects.filter(user__is_active=False).count()
    
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor")
        and request.user.gestor.cargo in ("diretor", "vice_diretor")
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
    
    return redirect("listar_desativados")

@login_required
@user_passes_test(is_super_ou_gestor)
def desativar_usuario(request, user_id):
    """Desativa um usuário (is_active=False) sem removê-lo do banco."""
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

# ==================== PROFESSORES ====================

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_professores(request):
    """Lista os professores cadastrados."""
    query = request.GET.get("q", "")
    professores = Professor.objects.all().select_related("user")
    if query:
        professores = professores.filter(nome_completo__icontains=query)
    return render(request, "professor/listar_professores.html", {
        "professores":    professores,
        "query":          query,
        "nome_exibicao":  get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_professor(request):
    """Novo professor e usuário."""
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            professor = form.save()
            messages.success(request, f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!")
            return redirect("listar_professores")
        for field, erros in form.errors.items():
            for erro in erros: messages.error(request, f"{field}: {erro}")
    else:
        form = ProfessorForm(request=request)
    return render(request, "professor/cadastrar_professor.html", {
        "form":            form,
        "professor":       None,
        "nome_exibicao":   get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_professor(request, professor_id):
    """Edita professor."""
    professor = get_object_or_404(Professor, id=professor_id)
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, instance=professor, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, f"Professor(a) {professor.nome_completo} atualizado(a) com sucesso!")
            return redirect("listar_professores")
        for field, erros in form.errors.items():
            for erro in erros: messages.error(request, f"{field}: {erro}")
    else:
        form = ProfessorForm(instance=professor, request=request)
    return render(request, "professor/cadastrar_professor.html", {
        "form":            form,
        "professor":       professor,
        "nome_exibicao":   get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

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

# ==================== ALUNOS ====================

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_alunos(request):
    """Lista alunos."""
    query = request.GET.get("q", "")
    alunos = Aluno.objects.all().select_related("user", "turma")
    if query:
        alunos = alunos.filter(nome_completo__icontains=query)
    return render(request, "aluno/listar_alunos.html", {
        "alunos":          alunos,
        "query":           query,
        "nome_exibicao":   get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_aluno(request):
    """Matrícula aluno."""
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(request, f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!")
            return redirect("listar_alunos")
    else:
        form = AlunoForm(request=request)
    return render(request, "aluno/cadastrar_aluno.html", {
        "form": form, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_aluno(request, aluno_id):
    """Edita prontuário."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado!")
            return redirect("listar_alunos")
    else:
        form = AlunoForm(instance=aluno, request=request)
    return render(request, "aluno/cadastrar_aluno.html", {
        "form": form, "aluno": aluno, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_aluno(request, aluno_id):
    """Remove aluno."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    try:
        if aluno.user: aluno.user.delete()
        else: aluno.delete()
        messages.success(request, "Aluno removido.")
    except Exception as e: messages.error(request, str(e))
    return redirect("listar_alunos")

# ==================== GESTORES ====================

@login_required
@user_passes_test(is_superuser)
def cadastrar_editar_gestor(request, gestor_id=None):
    """Dashboard Gestão."""
    gestor = get_object_or_404(Gestor, id=gestor_id) if gestor_id else None
    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, instance=gestor, request=request)
        if form.is_valid():
            gestor_obj = form.save()
            messages.success(request, f"{gestor_obj.nome_completo} processado!")
            return redirect("listar_gestores")
    else:
        form = GestorForm(instance=gestor, request=request)
    return render(request, "gestor/cadastrar_gestor.html", {
        "form": form, "gestor": gestor, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_superuser)
def listar_gestores(request):
    """Lista gestores."""
    query = request.GET.get("q", "")
    gestores = Gestor.objects.select_related("user").all()
    if query: gestores = gestores.filter(nome_completo__icontains=query)
    return render(request, "gestor/listar_gestores.html", {
        "gestores": gestores, "query": query, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_superuser)
def excluir_gestor(request, gestor_id):
    """Remove gestor."""
    gestor = get_object_or_404(Gestor, id=gestor_id)
    try:
        if gestor.user: gestor.user.delete()
        else: gestor.delete()
        messages.success(request, "Gestor removido.")
    except Exception as e: messages.error(request, str(e))
    return redirect("listar_gestores")

# ==================== TURMAS ====================

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_turmas(request):
    """Lista turmas."""
    ano_atual = timezone.localtime(timezone.now()).year
    query = request.GET.get("q", "").strip()
    anos_disponiveis = list(Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")) or [ano_atual]
    ano_filtro, anos_disponiveis = _get_anos_filtro(anos_disponiveis, request.GET.get("ano"), ano_atual)
    turmas = Turma.objects.filter(ano=ano_filtro)
    if query: turmas = turmas.filter(nome__icontains=query)
    return render(request, "turma/listar_turmas.html", {
        "turmas": turmas, "query": query, "ano_filtro": ano_filtro, "anos_disponiveis": anos_disponiveis, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_turma(request):
    """Cria turma."""
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))
    
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma cadastrada com sucesso!")
            return redirect("listar_turmas")
    else:
        # Pega o ano atual para facilitar o preenchimento inicial
        form = TurmaForm(initial={"ano": ano_atual})

    return render(request, "turma/cadastrar_turma.html", {
        "form": form,
        "anos": anos,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_turma(request, turma_id):
    """Edita turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("listar_turmas")
    else:
        form = TurmaForm(instance=turma)

    return render(request, "turma/cadastrar_turma.html", {
        "turma": turma,
        "form": form,
        "anos": anos,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_superuser)
def excluir_turma(request, turma_id):
    """Remove turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    nome = turma.nome
    turma.delete()
    messages.success(request, f"Turma {nome} removida.")
    return redirect("listar_turmas")

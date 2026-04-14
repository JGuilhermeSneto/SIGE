"""
Funções auxiliares de perfil: nome na UI, foto, redirecionamento por papel.

O que é: centraliza regras “quem é esse usuário no SIGE?” para views e
templates sem repetir ``hasattr``/``getattr`` espalhados.
"""

from django.templatetags.static import static


def get_nome_exibicao(user):
    """Retorna o nome para exibição (Primeiro Sobrenome ou E-mail)."""
    nome_auth = f"{user.first_name} {user.last_name}".strip()
    return nome_auth if nome_auth else user.email


def get_user_profile(user):
    """Identifica e retorna o objeto de perfil vinculado ao User."""
    for attr in ("gestor", "professor", "aluno"):
        p = getattr(user, attr, None)
        if p:
            return p
    return None


def get_foto_perfil(user):
    """Retorna a URL da foto de perfil ou imagem padrão."""
    for tipo in ("gestor", "professor", "aluno"):
        try:
            perfil = getattr(user, tipo, None)
            if perfil and getattr(perfil, "foto", None) and perfil.foto:
                return perfil.foto.url
        except Exception:
            continue
    return static("core/img/default-user.png")


def redirect_user(user):
    """Determina a URL de destino após login."""
    if user.is_superuser:
        return "painel_super"
    if hasattr(user, "gestor"):
        return "painel_gestor"
    if hasattr(user, "professor"):
        return "painel_professor"
    if hasattr(user, "aluno"):
        return "painel_aluno"
    return "painel_usuarios"

def is_super_ou_gestor(u):
    """Verifica se o usuário é superusuário ou gestor."""
    return u.is_superuser or hasattr(u, "gestor")

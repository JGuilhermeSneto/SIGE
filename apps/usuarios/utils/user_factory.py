"""Criação e vínculo de ``User`` aos perfis (senha padrão e validações)."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

PERFIL_LABEL = {
    "gestor": "gestor",
    "professor": "professor",
    "aluno": "aluno",
    "responsavel": "responsável",
}


def senha_padrao_cpf(username_digits: str) -> str:
    """Senha inicial (≥10 caracteres) derivada do CPF."""
    sufixo = (username_digits or "000000")[-6:].zfill(6)
    return f"Sige@{sufixo}"


def vincular_usuario_perfil(
    *,
    username: str,
    email: str,
    senha: str | None,
    perfil_attr: str,
    perfil_pk=None,
    is_staff: bool = False,
):
    """
    Obtém ou cria ``User`` para um perfil, evitando conflito de OneToOne.

    Raises:
        ValidationError: CPF/username já usado por outro tipo de perfil.
    """
    user = User.objects.filter(username=username).first()

    if user:
        perfil_atual = getattr(user, perfil_attr, None)
        if perfil_pk:
            if perfil_atual and perfil_atual.pk != perfil_pk:
                label = PERFIL_LABEL.get(perfil_attr, perfil_attr)
                raise ValidationError(
                    f"Este CPF já está cadastrado como {label} no sistema."
                )
        elif perfil_atual or any(
            getattr(user, p, None)
            for p in ("gestor", "professor", "aluno", "responsavel")
        ):
            raise ValidationError("Este CPF já está cadastrado no sistema.")

        for outro in ("gestor", "professor", "aluno", "responsavel"):
            if outro == perfil_attr:
                continue
            if getattr(user, outro, None) and not perfil_atual:
                label = PERFIL_LABEL.get(outro, outro)
                raise ValidationError(
                    f"Este CPF já está vinculado a um cadastro de {label}."
                )

        user.email = email
        if is_staff:
            user.is_staff = True
        if senha:
            validate_password(senha, user=user)
            user.set_password(senha)
        user.save()
        return user

    password = senha or senha_padrao_cpf(username)
    if senha:
        user = User(username=username, email=email, is_staff=is_staff)
        validate_password(senha, user=user)
        user.set_password(senha)
        user.save()
    else:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff,
        )
    return user

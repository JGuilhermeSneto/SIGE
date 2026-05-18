"""Utilitários compartilhados nas views de cadastro de perfis."""

from django.contrib import messages


def _label_campo(form, field_name: str) -> str:
    field = form.fields.get(field_name)
    if field and getattr(field, "label", None):
        return str(field.label)
    return field_name.replace("_", " ").title()


def exibir_erros_formulario(request, form, prefixo: str = "") -> None:
    """Exibe erros de formulário Django via ``messages``."""
    for field, erros in form.errors.items():
        for erro in erros:
            if field == "__all__":
                texto = str(erro)
            else:
                nome = _label_campo(form, field)
                texto = f"{nome}: {erro}"
            if prefixo:
                texto = f"{prefixo} — {texto}"
            messages.error(request, texto)


def exibir_erros_cadastro_aluno(request, form, form_saude) -> None:
    """Erros do aluno e da ficha médica no mesmo fluxo de matrícula."""
    if not form.is_valid():
        exibir_erros_formulario(request, form, "Dados do aluno")
    if not form_saude.is_valid():
        exibir_erros_formulario(request, form_saude, "Ficha médica")

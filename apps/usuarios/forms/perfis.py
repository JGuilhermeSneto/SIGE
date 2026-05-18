"""
Formulários ModelForm para cadastro/edição de Professor, Aluno e Gestor.

O que é: usa ``BaseModelForm`` para receber ``request`` e cria/atualiza
``User`` + perfil associado com validações de senha quando necessário.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.comum.forms.base_formularios import BaseModelForm
from ..models.perfis import Professor, Aluno, Gestor
from ..utils.user_factory import vincular_usuario_perfil

User = get_user_model()


def clean_cpf_to_username(cpf):
    """Limpa o CPF para usar como username (apenas números)."""
    if not cpf:
        return ""
    return "".join(filter(str.isdigit, cpf))


class ProfessorForm(BaseModelForm):
    """Formulário para Professor."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Se vazio, gera senha inicial no padrão Sige@XXXXXX (últimos 6 dígitos do CPF).",
    )
    senha_confirmacao = forms.CharField(
        required=False, widget=forms.PasswordInput(), label="Confirmar Senha"
    )

    class Meta:
        model = Professor
        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "telefone",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "logradouro",
            "numero",
            "complemento",
            "formacao",
            "especializacao",
            "area_atuacao",
            "foto",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not cpf:
            return cpf
        un = clean_cpf_to_username(cpf)
        qs = User.objects.filter(username=un)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado no sistema.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmacao = cleaned_data.get("senha_confirmacao")
        if senha and confirmacao and senha != confirmacao:
            self.add_error("senha_confirmacao", "As senhas não coincidem.")
        if senha:
            user = (
                self.instance.user
                if self.instance.pk and getattr(self.instance, "user", None)
                else User(username=clean_cpf_to_username(cleaned_data.get("cpf", "")))
            )
            try:
                validate_password(senha, user=user)
            except ValidationError as exc:
                self.add_error("senha", exc)
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            prof = super().save(commit=False)
            email = self.cleaned_data.get("email")
            senha = self.cleaned_data.get("senha") or None
            un = clean_cpf_to_username(prof.cpf)

            user = vincular_usuario_perfil(
                username=un,
                email=email,
                senha=senha,
                perfil_attr="professor",
                perfil_pk=prof.pk,
            )
            prof.user = user
            if commit:
                prof.save()
            return prof


class AlunoForm(BaseModelForm):
    """Formulário para Aluno."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Se vazio, gera senha inicial no padrão Sige@XXXXXX (últimos 6 dígitos do CPF).",
    )
    senha_confirmacao = forms.CharField(
        required=False, widget=forms.PasswordInput(), label="Confirmar Senha"
    )

    class Meta:
        model = Aluno
        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "naturalidade",
            "telefone",
            "responsavel1",
            "responsavel2",
            "turma",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "logradouro",
            "numero",
            "complemento",
            "possui_necessidade_especial",
            "descricao_necessidade",
            "foto",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not cpf:
            return cpf
        un = clean_cpf_to_username(cpf)
        qs = User.objects.filter(username=un)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado no sistema.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmacao = cleaned_data.get("senha_confirmacao")
        if senha and confirmacao and senha != confirmacao:
            self.add_error("senha_confirmacao", "As senhas não coincidem.")
        if senha:
            user = (
                self.instance.user
                if self.instance.pk and getattr(self.instance, "user", None)
                else User(username=clean_cpf_to_username(cleaned_data.get("cpf", "")))
            )
            try:
                validate_password(senha, user=user)
            except ValidationError as exc:
                self.add_error("senha", exc)
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            aluno = super().save(commit=False)
            email = self.cleaned_data.get("email")
            senha = self.cleaned_data.get("senha") or None
            un = clean_cpf_to_username(aluno.cpf)

            user = vincular_usuario_perfil(
                username=un,
                email=email,
                senha=senha,
                perfil_attr="aluno",
                perfil_pk=aluno.pk,
            )
            aluno.user = user
            if commit:
                aluno.save()
            return aluno


class GestorForm(BaseModelForm):
    """Formulário para Gestor."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Se vazio, gera senha inicial no padrão Sige@XXXXXX (últimos 6 dígitos do CPF).",
    )
    senha_confirmacao = forms.CharField(
        required=False, widget=forms.PasswordInput(), label="Confirmar Senha"
    )

    class Meta:
        model = Gestor
        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "cargo",
            "telefone",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "logradouro",
            "numero",
            "complemento",
            "foto",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail em uso.")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if not cpf:
            return cpf
        un = clean_cpf_to_username(cpf)
        qs = User.objects.filter(username=un)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este CPF já está cadastrado no sistema.")
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmacao = cleaned_data.get("senha_confirmacao")
        if senha and confirmacao and senha != confirmacao:
            self.add_error("senha_confirmacao", "As senhas não coincidem.")
        if senha:
            user = (
                self.instance.user
                if self.instance.pk and getattr(self.instance, "user", None)
                else User(username=clean_cpf_to_username(cleaned_data.get("cpf", "")))
            )
            try:
                validate_password(senha, user=user)
            except ValidationError as exc:
                self.add_error("senha", exc)
        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            gestor = super().save(commit=False)
            email = self.cleaned_data.get("email")
            senha = self.cleaned_data.get("senha") or None
            un = clean_cpf_to_username(gestor.cpf)

            user = vincular_usuario_perfil(
                username=un,
                email=email,
                senha=senha,
                perfil_attr="gestor",
                perfil_pk=gestor.pk,
                is_staff=True,
            )
            gestor.user = user
            if commit:
                gestor.save()
            return gestor

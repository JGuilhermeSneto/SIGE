"""
Forms para o aplicativo core.

Contém formulários de login, cadastro e gerenciamento de usuários e notas.
"""

# ===================== IMPORTS (TODOS NO TOPO) =====================

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Aluno, Disciplina, Gestor, Nota, Professor, Turma

# ===================== LOGIN =====================


class LoginForm(forms.Form):
    """Formulário para login de usuários."""

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    user = None  # Inicializa atributo para evitar W0201

    def clean(self):
        """Validação customizada do formulário de login."""
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise forms.ValidationError("E-mail não encontrado.") from exc

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise forms.ValidationError("Senha incorreta.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        """Retorna o usuário autenticado."""
        return self.user


# ===================== PROFESSOR =====================


class ProfessorForm(forms.ModelForm):
    """Formulário para cadastro/edição de professores."""

    email = forms.EmailField(required=True, label="E-mail")
    senha = forms.CharField(required=False, widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = "__all__"

    def clean_email(self):
        """Valida se o e-mail não está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email


# ===================== ALUNO =====================


class AlunoForm(forms.ModelForm):
    """Formulário para cadastro/edição de alunos."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Aluno
        fields = "__all__"

    def clean_email(self):
        """Valida se o e-mail não está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email


# ===================== DISCIPLINA =====================


class DisciplinaForm(forms.ModelForm):
    """Formulário para cadastro/edição de disciplinas."""

    class Meta:
        model = Disciplina
        fields = ["nome", "professor", "turma"]


# ===================== TURMA =====================


class TurmaForm(forms.ModelForm):
    """Formulário para cadastro/edição de turmas."""

    class Meta:
        model = Turma
        fields = ["nome", "turno", "ano"]


# ===================== NOTA =====================


class NotaForm(forms.ModelForm):
    """Formulário para cadastro/edição de notas."""

    class Meta:
        model = Nota
        fields = ["nota1", "nota2", "nota3", "nota4"]


# ===================== EDITAR PERFIL =====================


class EditarPerfilForm(forms.ModelForm):
    """Formulário para edição de perfil de usuário."""

    senha_atual = forms.CharField(required=False, widget=forms.PasswordInput)
    nova_senha = forms.CharField(required=False, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        """Valida se o e-mail não está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email


# ===================== GESTOR =====================


class GestorForm(forms.ModelForm):
    """Formulário para cadastro/edição de gestores."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput)
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Gestor
        fields = "__all__"

    def clean_email(self):
        """Valida se o e-mail não está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email
    
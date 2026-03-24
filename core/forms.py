# ===================== IMPORTS (TODOS NO TOPO) =====================

from django import forms  # Forms do Django para criar formulários
from django.contrib.auth import authenticate  # Para autenticar usuários
from django.contrib.auth.models import User  # Modelo de usuário do Django
from django.core.exceptions import \
    ValidationError  # Para lançar erros de validação

from .models import (Aluno, Disciplina, Gestor, Nota,  # Models do app core
                     Professor, Turma)

# ===================== LOGIN =====================


class LoginForm(forms.Form):
    # Campo de e-mail
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    # Campo de senha
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )

    def clean(self):
        """
        Validação customizada do formulário de login.
        Garante que o e-mail exista e que a senha esteja correta.
        """
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # Verifica se existe um usuário com este e-mail
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("E-mail não encontrado.")

        # Autentica o usuário com a senha fornecida
        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise forms.ValidationError("Senha incorreta.")

        self.user = user  # Armazena o usuário autenticado
        return self.cleaned_data

    def get_user(self):
        """Retorna o usuário autenticado."""
        return self.user


# ===================== PROFESSOR =====================


class ProfessorForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, label="E-mail"
    )  # Campo de e-mail obrigatório
    senha = forms.CharField(
        required=False, widget=forms.PasswordInput
    )  # Campo de senha opcional
    senha_confirmacao = forms.CharField(
        required=False, widget=forms.PasswordInput
    )  # Confirmação de senha

    class Meta:
        model = Professor
        fields = "__all__"  # Todos os campos do modelo

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
    class Meta:
        model = Disciplina
        fields = ["nome", "professor", "turma"]  # Campos obrigatórios


# ===================== TURMA =====================


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ["nome", "turno", "ano"]


# ===================== NOTA =====================


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["nota1", "nota2", "nota3", "nota4"]


# ===================== EDITAR PERFIL =====================


class EditarPerfilForm(forms.ModelForm):
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

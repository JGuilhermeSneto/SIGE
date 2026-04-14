"""
Formulários ModelForm para cadastro/edição de Professor, Aluno e Gestor.

O que é: usa ``BaseModelForm`` para receber ``request`` e cria/atualiza
``User`` + perfil associado com validações de senha quando necessário.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.comum.forms.base_formularios import BaseModelForm
from ..models.perfis import Professor, Aluno, Gestor

User = get_user_model()

class ProfessorForm(BaseModelForm):
    """Formulário para Professor."""
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = Professor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "telefone", "cep", "estado", 
            "cidade", "bairro", "logradouro", "numero", "complemento", 
            "formacao", "especializacao", "area_atuacao", "foto",
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
        if qs.exists(): raise ValidationError("E-mail em uso.")
        return email

    def save(self, commit=True):
        prof = super().save(commit=False)
        email, senha = self.cleaned_data.get("email"), self.cleaned_data.get("senha")
        un = prof.cpf.replace(".", "").replace("-", "")
        if prof.pk and getattr(prof, "user", None): user = prof.user
        else: user = User(username=un)
        user.username, user.email = un, email
        if senha: user.set_password(senha)
        user.save()
        prof.user = user
        if commit: prof.save()
        return prof

class AlunoForm(BaseModelForm):
    """Formulário para Aluno."""
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = Aluno
        fields = [
            "nome_completo", "cpf", "data_nascimento", "naturalidade", "telefone", 
            "responsavel1", "responsavel2", "turma", "cep", "estado", "cidade", 
            "bairro", "logradouro", "numero", "complemento", 
            "possui_necessidade_especial", "descricao_necessidade", "foto",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        aluno = super().save(commit=False)
        email, senha = self.cleaned_data.get("email"), self.cleaned_data.get("senha")
        un = aluno.cpf.replace(".", "").replace("-", "")
        if aluno.pk and getattr(aluno, "user", None): user = aluno.user
        else: user = User(username=un)
        user.username, user.email = un, email
        if senha: user.set_password(senha)
        user.save()
        aluno.user = user
        if commit: aluno.save()
        return aluno

class GestorForm(BaseModelForm):
    """Formulário para Gestor."""
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = Gestor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "cargo", "telefone", 
            "cep", "estado", "cidade", "bairro", "logradouro", "numero", 
            "complemento", "foto",
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        gestor = super().save(commit=False)
        email, senha = self.cleaned_data.get("email"), self.cleaned_data.get("senha")
        un = gestor.cpf.replace(".", "").replace("-", "")
        if gestor.pk and getattr(gestor, "user", None): user = gestor.user
        else: user = User(username=un)
        user.username, user.email = un, email
        if senha: user.set_password(senha)
        user.save()
        gestor.user = user
        if commit: gestor.save()
        return gestor

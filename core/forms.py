"""
Módulo de formulários da aplicação core.

Define formulários para autenticação e cadastro/edição de usuários:
- LoginForm: autenticação por e-mail
- BaseModelForm: base para formulários de modelos vinculados ao User
- ProfessorForm, AlunoForm, GestorForm: criação/edição de usuários e perfis
- EditarPerfilForm: alteração de e-mail e senha
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from .models import Aluno, Gestor, Professor

User = get_user_model()

# ==========================================================
# FORMULÁRIO DE LOGIN
# ==========================================================
class LoginForm(forms.Form):
    """
    Formulário de login utilizando e-mail e senha.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    user = None  # Armazena o usuário autenticado

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise ValidationError("E-mail e senha são obrigatórios.")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise ValidationError("E-mail não encontrado.") from exc

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise ValidationError("Senha incorreta.")

        self.user = user
        return cleaned_data

    def get_user(self):
        """Retorna o usuário autenticado após validação bem-sucedida."""
        return self.user

# ==========================================================
# FORMULÁRIO BASE PARA MODELS
# ==========================================================
class BaseModelForm(forms.ModelForm):
    """
    Formulário base para os models vinculados a um usuário.
    Permite capturar a request caso seja necessário no formulário.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

# ==========================================================
# FORMULÁRIO PROFESSOR
# ==========================================================
class ProfessorForm(BaseModelForm):
    """
    Formulário para criação/edição de Professor, incluindo:
    - Campos do modelo Professor
    - Email e senha do usuário vinculado
    """
    email = forms.EmailField(required=True, help_text="E-mail do professor")
    senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Senha do usuário")
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Confirmação de senha")

    class Meta:
        model = Professor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "telefone",
            "cep", "estado", "cidade", "bairro", "logradouro",
            "numero", "complemento", "formacao", "especializacao",
            "area_atuacao", "foto"
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche o email se o usuário já existir
        if self.instance and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        """Valida se o e-mail já está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail já está em uso por outro usuário.")
        return email

    def clean(self):
        """Valida senhas e CPF para criação/edição do usuário."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        cpf = cleaned_data.get("cpf")

        # Validação de senha
        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        # Validação de CPF único para o username
        if cpf:
            username = cpf.replace(".", "").replace("-", "")
            qs = User.objects.filter(username=username)
            if self.instance.pk and getattr(self.instance, "user", None):
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise ValidationError("Já existe um usuário cadastrado com este CPF.")

        return cleaned_data

    def save(self, commit=True):
        """
        Cria ou atualiza o usuário vinculado ao professor.
        """
        professor = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        username = professor.cpf.replace(".", "").replace("-", "")

        if professor.pk and getattr(professor, "user", None):
            user = professor.user
        else:
            user = User(username=username)

        user.username = username
        user.email = email

        if senha:
            user.set_password(senha)
        elif not user.pk:
            user.set_unusable_password()

        user.save()
        professor.user = user

        if commit:
            professor.save()
        return professor

# ==========================================================
# FORMULÁRIO ALUNO
# ==========================================================
class AlunoForm(BaseModelForm):
    """
    Formulário para criação/edição de Aluno, incluindo:
    - Campos do modelo Aluno
    - Email e senha do usuário vinculado
    """
    email = forms.EmailField(required=True, help_text="E-mail do aluno")
    senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Senha do usuário")
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Confirmação de senha")

    class Meta:
        model = Aluno
        fields = [
            "nome_completo", "cpf", "data_nascimento", "naturalidade",
            "telefone", "responsavel1", "responsavel2", "turma",
            "cep", "estado", "cidade", "bairro", "logradouro",
            "numero", "complemento", "possui_necessidade_especial",
            "descricao_necessidade", "foto"
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        """Valida se o e-mail já está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail já está em uso.")
        return email

    def clean(self):
        """Valida senhas e necessidade especial do aluno."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        possui = cleaned_data.get("possui_necessidade_especial")
        desc = cleaned_data.get("descricao_necessidade")

        # Validação de senha
        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        # Validação da necessidade especial
        if possui and not desc:
            raise ValidationError("É obrigatório descrever a necessidade especial informada.")

        return cleaned_data

    def save(self, commit=True):
        """Cria ou atualiza o usuário vinculado ao aluno."""
        aluno = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        username = aluno.cpf.replace(".", "").replace("-", "")

        if aluno.pk and getattr(aluno, "user", None):
            user = aluno.user
        else:
            user = User(username=username)

        user.username = username
        user.email = email

        if senha:
            user.set_password(senha)
        elif not aluno.pk:
            user.set_unusable_password()

        user.save()
        aluno.user = user

        if commit:
            aluno.save()
        return aluno

# ==========================================================
# FORMULÁRIO GESTOR
# ==========================================================
class GestorForm(BaseModelForm):
    """
    Formulário para criação/edição de Gestor, incluindo:
    - Campos do modelo Gestor
    - Email e senha do usuário vinculado
    """
    email = forms.EmailField(required=True, help_text="E-mail do gestor")
    senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Senha do usuário")
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Confirmação de senha")

    class Meta:
        model = Gestor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "cargo",
            "telefone", "cep", "estado", "cidade", "bairro",
            "logradouro", "numero", "complemento", "foto"
        ]
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        """Valida se o e-mail já está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail já está em uso por outro usuário.")
        return email

    def clean(self):
        """Valida senhas e CPF do gestor."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        cpf = cleaned_data.get("cpf")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        if cpf:
            username = cpf.replace(".", "").replace("-", "")
            qs = User.objects.filter(username=username)
            if self.instance.pk and getattr(self.instance, "user", None):
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise ValidationError("Já existe um usuário cadastrado com este CPF.")

        return cleaned_data

    def save(self, commit=True):
        """Cria ou atualiza o usuário vinculado ao gestor."""
        gestor = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")
        username = gestor.cpf.replace(".", "").replace("-", "")

        if gestor.pk and getattr(gestor, "user", None):
            user = gestor.user
        else:
            user = User(username=username)

        user.username = username
        user.email = email

        if senha:
            user.set_password(senha)
        elif not gestor.pk:
            user.set_unusable_password()

        user.save()
        gestor.user = user

        if commit:
            gestor.save()
        return gestor

# ==========================================================
# FORMULÁRIO EDITAR PERFIL
# ==========================================================
class EditarPerfilForm(forms.ModelForm):
    """
    Formulário para edição do perfil do usuário autenticado:
    - Alteração de e-mail
    - Alteração de senha
    """
    nova_senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Nova senha")
    confirmar_senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Confirmação da nova senha")

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        """Valida se o e-mail já está em uso por outro usuário."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("E-mail já está em uso.")
        return email

    def clean(self):
        """Valida se as novas senhas coincidem e atendem o tamanho mínimo."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("nova_senha")
        conf = cleaned_data.get("confirmar_senha")

        if senha or conf:
            if senha != conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        return cleaned_data

    def save(self, commit=True):
        """Atualiza o usuário com a nova senha e e-mail, se fornecidos."""
        user = super().save(commit=False)
        senha = self.cleaned_data.get("nova_senha")
        if senha:
            user.set_password(senha)
        if commit:
            user.save()
        return user
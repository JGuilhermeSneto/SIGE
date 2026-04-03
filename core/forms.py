"""
Módulo de formulários da aplicação core.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

from .models import Aluno, Gestor, Professor

User = get_user_model()


# =====================================================================
# Formulário de Autenticação
# =====================================================================


class LoginForm(forms.Form):
    """Formulário de autenticação por e-mail e senha."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )

    user = None

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
        return self.user


# =====================================================================
# Formulário Base
# =====================================================================


class BaseModelForm(forms.ModelForm):
    """Formulário base que aceita o parâmetro request durante a inicialização."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


# =====================================================================
# Formulário de Professor
# =====================================================================


class ProfessorForm(BaseModelForm):
    """Formulário de cadastro e edição de professores."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

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
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    # FIX: ProfessorForm não tinha clean_email — e-mail duplicado causava
    # IntegrityError silenciosa que impedia o save sem mensagem clara ao usuário
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail já está em uso por outro usuário.")
        return email

    def clean(self):
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


# =====================================================================
# Formulário de Aluno
# =====================================================================


class AlunoForm(BaseModelForm):
    """Formulário de cadastro e edição de aluno."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

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
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

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
            raise ValidationError("E-mail já em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        possui = cleaned_data.get("possui_necessidade_especial")
        desc = cleaned_data.get("descricao_necessidade")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        if possui and not desc:
            raise ValidationError(
                "É obrigatório descrever a necessidade especial informada."
            )

        return cleaned_data

    def save(self, commit=True):
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
        elif not user.pk:
            user.set_unusable_password()

        user.save()
        aluno.user = user

        if commit:
            aluno.save()

        return aluno


# =====================================================================
# Formulário de Gestor
# =====================================================================


class GestorForm(BaseModelForm):
    """Formulário de cadastro e edição de gestor."""

    email = forms.EmailField(required=True)
    senha = forms.CharField(required=False, widget=forms.PasswordInput())
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = Gestor
        # FIX: data_nascimento adicionado (campo existia no template mas não no form/model)
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
        widgets = {
            # FIX: widget com type="date" para o campo data_nascimento funcionar no browser
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    # FIX: GestorForm não tinha clean_email — e-mail duplicado causava falha silenciosa
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("E-mail já está em uso por outro usuário.")
        return email

    def clean(self):
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
                raise ValidationError(
                    "Já existe um usuário cadastrado com este CPF. "
                    "Verifique o número informado."
                )

        return cleaned_data

    def save(self, commit=True):
        gestor = super().save(commit=False)
        email = self.cleaned_data.get("email", "")
        senha = self.cleaned_data.get("senha")
        username = gestor.cpf.replace(".", "").replace("-", "")

        user_existente = None
        if gestor.pk:
            try:
                user_existente = User.objects.get(gestor__pk=gestor.pk)
            except User.DoesNotExist:
                user_existente = None

        if user_existente:
            user = user_existente
        else:
            user = User(username=username)

        user.username = username
        user.email = email

        if senha:
            user.set_password(senha)
        elif not user.pk:
            user.set_unusable_password()

        user.save()
        gestor.user = user

        if commit:
            gestor.save()

        return gestor


# =====================================================================
# Formulário de Edição de Perfil
# =====================================================================


class EditarPerfilForm(forms.ModelForm):
    """Formulário para edição de e-mail e senha do usuário autenticado."""

    nova_senha = forms.CharField(required=False, widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("E-mail já está em uso.")
        return email

    def clean(self):
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
        user = super().save(commit=False)
        senha = self.cleaned_data.get("nova_senha")
        if senha:
            user.set_password(senha)
        if commit:
            user.save()
        return user
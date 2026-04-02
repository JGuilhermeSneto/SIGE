"""
Módulo de formulários da aplicação core.

Define os formulários de autenticação e cadastro para os modelos
Professor, Aluno e Gestor, incluindo validações personalizadas e
criação/atualização automática do usuário (User) vinculado.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from .models import Aluno, Gestor, Professor

User = get_user_model()


# ======================= Login =======================

class LoginForm(forms.Form):
    """Formulário de autenticação por e-mail e senha."""

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    user = None  # Armazena o usuário autenticado após validação bem-sucedida

    def clean(self):
        """Valida as credenciais e autentica o usuário."""
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

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
        return self.cleaned_data

    def get_user(self):
        """Retorna o usuário autenticado após a validação do formulário."""
        return self.user


# ======================= BaseModelForm =======================

class BaseModelForm(forms.ModelForm):
    """Form base que aceita o objeto request no __init__."""

    def __init__(self, *args, **kwargs):
        """Remove o argumento 'request' antes de repassar ao ModelForm."""
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


# ======================= Professor =======================

class ProfessorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de professores,
    incluindo criação e atualização do usuário vinculado.
    """

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Digite o e-mail"}),
    )
    senha = forms.CharField(
        label="Senha",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite a senha"}),
    )
    senha_confirmacao = forms.CharField(
        label="Confirmação de senha",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    class Meta:
        model = Professor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "telefone", "cep", "estado",
            "cidade", "bairro", "logradouro", "numero", "complemento",
            "formacao", "especializacao", "area_atuacao", "foto",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}, format="%d-%m-%Y")
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.instance and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

        if self.instance and self.instance.data_nascimento:
            self.initial["data_nascimento"] = self.instance.data_nascimento.strftime("%Y-%m-%d")

    def clean(self):
        """Valida senha e unicidade do CPF."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_confirmacao = cleaned_data.get("senha_confirmacao")
        cpf = cleaned_data.get("cpf")

        if senha or senha_confirmacao:
            if not senha or not senha_confirmacao:
                raise ValidationError("Para definir uma senha, ambos os campos devem ser preenchidos.")
            if senha != senha_confirmacao:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve conter no mínimo 6 caracteres.")

        if cpf:
            username = cpf.replace(".", "").replace("-", "")
            user_qs = User.objects.filter(username=username)
            if self.instance.pk and getattr(self.instance, "user", None):
                user_qs = user_qs.exclude(pk=self.instance.user.pk)
            if user_qs.exists():
                raise ValidationError("Já existe um usuário cadastrado com este CPF.")

        return cleaned_data

    def save(self, commit=True):
        """Cria ou atualiza o usuário vinculado ao professor."""
        professor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")
        email = self.cleaned_data.get("email")
        username = professor.cpf.replace(".", "").replace("-", "")

        if professor.pk and getattr(professor, "user", None):
            user = professor.user
            user.username = username
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            if senha:
                user = User.objects.create_user(username=username, email=email, password=senha)
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_unusable_password()
                user.save()
            professor.user = user

        if commit:
            professor.save()

        return professor


# ======================= Aluno =======================

class AlunoForm(BaseModelForm):
    """Formulário de cadastro e edição de Aluno."""

    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"placeholder": "E-mail", "class": "form-control"})
    )
    senha = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={"placeholder": "Senha", "class": "form-control"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha", "class": "form-control"}),
    )

    class Meta:
        model = Aluno
        fields = [
            "nome_completo", "cpf", "data_nascimento", "naturalidade", "telefone",
            "responsavel1", "responsavel2", "turma", "cep", "estado", "cidade",
            "bairro", "logradouro", "numero", "complemento",
            "possui_necessidade_especial", "descricao_necessidade", "foto",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "cpf": forms.TextInput(attrs={"placeholder": "000.000.000-00", "class": "form-control"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000", "class": "form-control"}),
            "cep": forms.TextInput(attrs={"placeholder": "00000-000", "class": "form-control"}),
            "cidade": forms.TextInput(attrs={"placeholder": "Cidade", "class": "form-control"}),
            "bairro": forms.TextInput(attrs={"placeholder": "Bairro", "class": "form-control"}),
            "logradouro": forms.TextInput(attrs={"placeholder": "Rua / Avenida", "class": "form-control"}),
            "numero": forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            "filiacao_1": forms.TextInput(attrs={"placeholder": "Nome do responsável 1", "class": "form-control"}),
            "filiacao_2": forms.TextInput(attrs={"placeholder": "Nome do responsável 2", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.instance.pk and getattr(self.instance, "user", None):
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and getattr(self.instance, "user", None):
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        possui_necessidade = cleaned_data.get("possui_necessidade_especial")
        descricao = cleaned_data.get("descricao_necessidade")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        if possui_necessidade and not descricao:
            raise ValidationError("Descreva a necessidade especial do aluno.")

        return cleaned_data

    def save(self, commit=True):
        aluno = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")

        if hasattr(aluno, "user") and aluno.user:
            user = aluno.user
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            username = aluno.nome_completo.replace(" ", "").lower()
            user = User.objects.create_user(username=username, email=email, password=senha or None)
            aluno.user = user

        if commit:
            aluno.save()
        return aluno


# ======================= Gestor =======================

class GestorForm(BaseModelForm):
    """Formulário de cadastro e edição de Gestor."""

    senha = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}))

    class Meta:
        model = Gestor
        fields = [
            "nome_completo", "cpf", "data_nascimento", "telefone", "email",
            "cep", "uf", "cidade", "endereco", "cargo", "foto",
        ]

    def clean(self):
        """Valida regras de senha do Gestor."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")
            if not any(c.isupper() for c in senha):
                raise ValidationError("A senha deve conter ao menos uma letra maiúscula.")
            if not any(c.islower() for c in senha):
                raise ValidationError("A senha deve conter ao menos uma letra minúscula.")
            if not any(c.isdigit() for c in senha):
                raise ValidationError("A senha deve conter ao menos um número.")

        return cleaned_data

    def save(self, commit=True):
        """Cria ou atualiza Gestor e User vinculado."""
        gestor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")
        user = getattr(gestor, "user", None)

        if not user:
            base_username = gestor.cpf.replace(".", "").replace("-", "")
            username = base_username
            contador = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{contador}"
                contador += 1

            user = User.objects.create_user(username=username, email=gestor.email, password=senha if senha else None)
            gestor.user = user
        elif senha:
            user.set_password(senha)

        user.email = gestor.email
        user.save()

        if commit:
            gestor.save()

        return gestor


# ======================= Editar Perfil =======================

class EditarPerfilForm(forms.ModelForm):
    """Formulário para o usuário editar seu próprio perfil (e-mail e senha)."""

    nova_senha = forms.CharField(required=False, widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                raise ValidationError("As senhas não coincidem.")
            if nova_senha and len(nova_senha) < 6:
                raise ValidationError("A senha deve ter ao menos 6 caracteres.")

        return cleaned_data 
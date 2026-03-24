from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from .models import Professor, Aluno, Gestor

User = get_user_model()


# ======================= Login =======================
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    user = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if not email or not password:
            raise ValidationError("E-mail e senha são obrigatórios.")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("E-mail não encontrado.")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise ValidationError("Senha incorreta.")

        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user


# ======================= BaseForm com request =======================
class BaseModelForm(forms.ModelForm):
    """Form base que aceita request no __init__"""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


# ======================= Professor =======================
class ProfessorForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"})
    )

    class Meta:
        model = Professor
        fields = [
            "nome_completo", "cpf", "telefone", "data_nascimento",
            "cep", "bairro", "logradouro", "numero", "complemento",
            "estado", "cidade", "formacao", "especializacao",
            "area_atuacao", "foto"
        ]

    def __init__(self, *args, **kwargs):
        # Pega request se passado, evita erro de argumento inesperado
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Preencher email se o user já existe
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

        # Placeholders ou máscaras extras
        self.fields["cpf"].widget.attrs.update({"placeholder": "000.000.000-00"})
        self.fields["telefone"].widget.attrs.update({"placeholder": "(00) 00000-0000"})
        self.fields["cep"].widget.attrs.update({"placeholder": "00000-000"})
        self.fields["cidade"].widget.attrs.update({"placeholder": "Digite a cidade"})
        self.fields["bairro"].widget.attrs.update({"placeholder": "Digite o bairro"})
        self.fields["logradouro"].widget.attrs.update({"placeholder": "Digite o logradouro"})
        self.fields["numero"].widget.attrs.update({"placeholder": "Número"})
        self.fields["complemento"].widget.attrs.update({"placeholder": "Complemento"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve ter ao menos 6 caracteres.")
            if not any(c.isupper() for c in senha):
                raise ValidationError("A senha deve ter ao menos uma letra maiúscula.")
            if not any(c.islower() for c in senha):
                raise ValidationError("A senha deve ter ao menos uma letra minúscula.")
            if not any(c.isdigit() for c in senha):
                raise ValidationError("A senha deve ter ao menos um número.")

        return cleaned_data

    def save(self, commit=True):
        professor = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")

        # Cria ou atualiza User relacionado
        if hasattr(professor, "user") and professor.user:
            user = professor.user
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            username = professor.nome_completo.replace(" ", "").lower()
            user = User.objects.create_user(username=username, email=email, password=senha or None)
            professor.user = user

        if commit:
            professor.save()
        return professor

# ======================= Aluno =======================

class AlunoForm(BaseModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )

    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"})
    )

    class Meta:
        model = Aluno
        fields = [
            # Dados pessoais
            "nome_completo", "cpf", "data_nascimento", "naturalidade",

            # Contato
            "telefone",

            # Filiação
            "filiacao1", "filiacao2",

            # Escolar
            "turma",

            # Endereço
            "cep", "estado", "cidade", "bairro",
            "logradouro", "numero", "complemento",

            # Necessidades especiais
            "possui_necessidade_especial", "descricao_necessidade",

            # Outros
            "foto"
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Preencher email se já existir user
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

        # Placeholders úteis
        self.fields["cpf"].widget.attrs.update({"placeholder": "000.000.000-00"})
        self.fields["telefone"].widget.attrs.update({"placeholder": "(00) 00000-0000"})
        self.fields["cep"].widget.attrs.update({"placeholder": "00000-000"})
        self.fields["cidade"].widget.attrs.update({"placeholder": "Cidade"})
        self.fields["bairro"].widget.attrs.update({"placeholder": "Bairro"})
        self.fields["logradouro"].widget.attrs.update({"placeholder": "Rua / Avenida"})
        self.fields["numero"].widget.attrs.update({"placeholder": "Número"})

    # ================= EMAIL =================
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)

        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    # ================= VALIDAÇÕES =================
    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        possui_necessidade = cleaned_data.get("possui_necessidade_especial")
        descricao = cleaned_data.get("descricao_necessidade")

        # Validação de senha
        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        # Validação de necessidade especial
        if possui_necessidade and not descricao:
            raise ValidationError("Descreva a necessidade especial do aluno.")

        return cleaned_data

    # ================= SAVE =================
    def save(self, commit=True):
        aluno = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")

        # Criação/atualização do User
        if hasattr(aluno, "user") and aluno.user:
            user = aluno.user
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            username = aluno.nome_completo.replace(" ", "").lower()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha or None
            )
            aluno.user = user

        if commit:
            aluno.save()

        return aluno


# ======================= Gestor =======================
class GestorForm(BaseModelForm):
    senha = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    senha_confirmacao = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}))

    class Meta:
        model = Gestor
        fields = ["nome_completo", "cpf", "cargo", "uf", "cidade", "endereco", "foto"]

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if senha and len(senha) < 6:
                raise ValidationError("A senha deve ter ao menos 6 caracteres.")
        return cleaned_data

    def save(self, commit=True):
        gestor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")
        if senha:
            if hasattr(gestor, "user") and gestor.user:
                gestor.user.set_password(senha)
                gestor.user.save()
            else:
                username = gestor.nome_completo.replace(" ", "").lower()
                user = User.objects.create_user(username=username, email="", password=senha)
                gestor.user = user
        if commit:
            gestor.save()
        return gestor


# ======================= Editar Perfil =======================
class EditarPerfilForm(forms.ModelForm):
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
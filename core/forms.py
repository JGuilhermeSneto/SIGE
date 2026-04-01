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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    # Armazena o usuário autenticado após validação bem-sucedida
    user = None

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


# ======================= BaseForm com request =======================


class BaseModelForm(forms.ModelForm):
    """Form base que aceita o objeto request no __init__."""

    def __init__(self, *args, **kwargs):
        """Remove o argumento 'request' antes de repassar ao ModelForm."""
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


# ======================= Professor =======================


# Obtém o modelo de usuário configurado no projeto
User = get_user_model()


class ProfessorForm(forms.ModelForm):
    """
    Formulário responsável pelo cadastro e edição de professores.

    Este formulário abstrai a criação e atualização do modelo Professor,
    incluindo o gerenciamento do usuário autenticável (User) vinculado.
    """

    # ======================================================
    # CAMPOS AUXILIARES (NÃO PERSISTIDOS NO MODEL)
    # ======================================================

    senha = forms.CharField(
        label="Senha",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite a senha"}),
        help_text="Informe uma senha para acesso ao sistema.",
    )

    senha_confirmacao = forms.CharField(
        label="Confirmação de senha",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
        help_text="Repita a senha para confirmação.",
    )

    # ======================================================
    # CONFIGURAÇÃO DO MODELFORM
    # ======================================================
    class Meta:
        """
        Define o modelo base do formulário e os campos expostos
        para preenchimento pelo usuário.
        """

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

    # ======================================================
    # VALIDAÇÕES CUSTOMIZADAS
    # ======================================================
    def clean(self):
        """
        Realiza validações globais do formulário.

        Regras aplicadas:
        - Caso uma senha seja informada, a confirmação é obrigatória
        - As senhas devem ser idênticas
        - A senha deve possuir no mínimo 6 caracteres
        """
        cleaned_data = super().clean()

        senha = cleaned_data.get("senha")
        senha_confirmacao = cleaned_data.get("senha_confirmacao")

        # Validação condicional: só valida se houver tentativa de definir senha
        if senha or senha_confirmacao:
            if not senha or not senha_confirmacao:
                raise ValidationError(
                    "Para definir uma senha, ambos os campos devem ser preenchidos."
                )

            if senha != senha_confirmacao:
                raise ValidationError("As senhas informadas não coincidem.")

            if len(senha) < 6:
                raise ValidationError("A senha deve conter no mínimo 6 caracteres.")

        return cleaned_data

    # ======================================================
    # PERSISTÊNCIA CUSTOMIZADA
    # ======================================================
    def save(self, commit=True):
        """
        Persiste o objeto Professor e gerencia o usuário vinculado.

        Comportamento:
        - Se o Professor já possui um User, apenas redefine a senha
        - Caso contrário, cria um novo User automaticamente
        - O username é derivado do CPF para garantir unicidade
        """
        professor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")

        # Criação ou atualização do usuário somente se senha for informada
        if senha:
            if professor.pk and hasattr(professor, "user") and professor.user:
                # Atualiza senha de usuário existente
                professor.user.set_password(senha)
                professor.user.save()
            else:
                # Cria novo usuário para o professor
                username = professor.cpf.replace(".", "").replace("-", "")
                user = User.objects.create_user(username=username, password=senha)
                professor.user = user

        # Salva o professor no banco de dados
        if commit:
            professor.save()

        return professor


# ======================= Aluno =======================


class AlunoForm(BaseModelForm):
    """Formulário de cadastro e edição de Aluno."""

    # E-mail pertence ao User vinculado, não ao modelo Aluno
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )
    # Senha opcional para permitir edição sem redefinir a senha
    senha = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    class Meta:
        """Configuração de modelo e campos do AlunoForm."""

        model = Aluno
        fields = [
            # Dados pessoais
            "nome_completo",
            "cpf",
            "data_nascimento",
            "naturalidade",
            # Contato
            "telefone",
            # Filiação
            "filiacao1",
            "filiacao2",
            # Escolar
            "turma",
            # Endereço
            "cep",
            "estado",
            "cidade",
            "bairro",
            "logradouro",
            "numero",
            "complemento",
            # Necessidades especiais
            "possui_necessidade_especial",
            "descricao_necessidade",
            # Outros
            "foto",
        ]

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário.

        - Remove 'request' dos kwargs.
        - Preenche o e-mail quando o Aluno já possui um User vinculado.
        - Configura placeholders para todos os campos de endereço e contato.
        """
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Preencher e-mail se já existir User vinculado ao Aluno
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

        # Placeholders para campos de dados pessoais e endereço
        self.fields["cpf"].widget.attrs.update({"placeholder": "000.000.000-00"})
        self.fields["telefone"].widget.attrs.update({"placeholder": "(00) 00000-0000"})
        self.fields["cep"].widget.attrs.update({"placeholder": "00000-000"})
        self.fields["cidade"].widget.attrs.update({"placeholder": "Cidade"})
        self.fields["bairro"].widget.attrs.update({"placeholder": "Bairro"})
        self.fields["logradouro"].widget.attrs.update({"placeholder": "Rua / Avenida"})
        self.fields["numero"].widget.attrs.update({"placeholder": "Número"})

    def clean_email(self):
        """
        Valida unicidade do e-mail.

        Na edição, exclui da verificação o e-mail atual do próprio
        usuário vinculado ao Aluno.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)

        # Exclui o próprio usuário ao editar
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        """
        Validações gerais do formulário de Aluno.

        - Verifica correspondência e tamanho mínimo da senha.
        - Exige descrição da necessidade especial quando marcada.
        """
        cleaned_data = super().clean()

        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")
        possui_necessidade = cleaned_data.get("possui_necessidade_especial")
        descricao = cleaned_data.get("descricao_necessidade")

        # Validação de senha: apenas quando ao menos um campo for preenchido
        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")
            if len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

        # Necessidade especial requer descrição detalhada
        if possui_necessidade and not descricao:
            raise ValidationError("Descreva a necessidade especial do aluno.")

        return cleaned_data

    def save(self, commit=True):
        """
        Salva o Aluno e cria ou atualiza o User vinculado.

        - Atualiza e-mail e senha do User existente quando em modo edição.
        - Cria um novo User com username derivado do nome completo no cadastro.
        """
        aluno = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")

        if hasattr(aluno, "user") and aluno.user:
            # Atualiza o User já vinculado ao Aluno
            user = aluno.user
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            # Cria novo User com username baseado no nome completo
            username = aluno.nome_completo.replace(" ", "").lower()
            user = User.objects.create_user(
                username=username, email=email, password=senha or None
            )
            aluno.user = user

        if commit:
            aluno.save()

        return aluno


# ======================= Gestor =======================


User = get_user_model()


class GestorForm(BaseModelForm):
    """Formulário de cadastro e edição de Gestor."""

    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"}),
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    class Meta:
        model = Gestor
        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "telefone",
            "email",
            "cep",
            "uf",
            "cidade",
            "endereco",
            "cargo",
            "foto",
        ]

    def clean(self):
        """Valida regras de senha."""
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        senha_conf = cleaned_data.get("senha_confirmacao")

        if senha or senha_conf:
            if senha != senha_conf:
                raise ValidationError("As senhas não coincidem.")

            if len(senha) < 6:
                raise ValidationError("A senha deve ter no mínimo 6 caracteres.")

            if not any(c.isupper() for c in senha):
                raise ValidationError(
                    "A senha deve conter ao menos uma letra maiúscula."
                )

            if not any(c.islower() for c in senha):
                raise ValidationError(
                    "A senha deve conter ao menos uma letra minúscula."
                )

            if not any(c.isdigit() for c in senha):
                raise ValidationError("A senha deve conter ao menos um número.")

        return cleaned_data

    def save(self, commit=True):
        """Cria ou atualiza Gestor e User vinculado."""
        gestor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")

        if gestor.pk:
            user = gestor.user
        else:
            user = None

        if not user:
            # Criação de usuário novo
            base_username = gestor.cpf.replace(".", "").replace("-", "")
            username = base_username

            contador = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{contador}"
                contador += 1

            user = User.objects.create_user(
                username=username,
                email=gestor.email,
                password=senha if senha else None,
            )
            gestor.user = user

        elif senha:
            # Atualização de senha
            user.set_password(senha)

        # Mantém e-mail sincronizado
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
        """Configuração de modelo e campos do EditarPerfilForm."""

        model = User
        fields = ["email"]

    def clean_email(self):
        """
        Valida unicidade do e-mail excluindo o próprio usuário logado.

        Impede que outro usuário já cadastrado utilize o mesmo endereço.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        """
        Valida os campos de nova senha.

        - Nova senha e confirmação devem ser iguais.
        - A nova senha deve ter no mínimo 6 caracteres.
        """
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                raise ValidationError("As senhas não coincidem.")
            if nova_senha and len(nova_senha) < 6:
                raise ValidationError("A senha deve ter ao menos 6 caracteres.")
        return cleaned_data

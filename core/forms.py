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


class ProfessorForm(forms.ModelForm):
    """Formulário de cadastro e edição de Professor."""

    # Campo de e-mail separado pois pertence ao modelo User, não ao Professor
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "E-mail"})
    )
    # Senha e confirmação são opcionais na edição; obrigatórios apenas no cadastro
    senha = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    class Meta:
        """Configuração de modelo e campos do ProfessorForm."""

        model = Professor
        fields = [
            "nome_completo",
            "cpf",
            "telefone",
            "data_nascimento",
            "cep",
            "bairro",
            "logradouro",
            "numero",
            "complemento",
            "estado",
            "cidade",
            "formacao",
            "especializacao",
            "area_atuacao",
            "foto",
        ]

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário.

        - Remove 'request' dos kwargs para evitar erro de argumento inesperado.
        - Preenche o campo 'email' com o e-mail do usuário vinculado (modo edição).
        - Adiciona placeholders e atributos de máscara nos campos de endereço.
        """
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Preencher e-mail se o User vinculado ao Professor já existir
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

        # Adiciona placeholders para melhor UX nos campos de dados pessoais/endereço
        self.fields["cpf"].widget.attrs.update({"placeholder": "000.000.000-00"})
        self.fields["telefone"].widget.attrs.update({"placeholder": "(00) 00000-0000"})
        self.fields["cep"].widget.attrs.update({"placeholder": "00000-000"})
        self.fields["cidade"].widget.attrs.update({"placeholder": "Digite a cidade"})
        self.fields["bairro"].widget.attrs.update({"placeholder": "Digite o bairro"})
        self.fields["logradouro"].widget.attrs.update(
            {"placeholder": "Digite o logradouro"}
        )
        self.fields["numero"].widget.attrs.update({"placeholder": "Número"})
        self.fields["complemento"].widget.attrs.update({"placeholder": "Complemento"})

    def clean_email(self):
        """
        Valida unicidade do e-mail no sistema.

        Exclui da verificação o próprio usuário vinculado ao Professor
        quando estiver em modo de edição.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)

        # Na edição, ignora o e-mail atual do próprio usuário
        if self.instance.pk and hasattr(self.instance, "user") and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)

        if qs.exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean(self):
        """
        Valida os campos de senha.

        Regras aplicadas:
        - Senha e confirmação devem ser iguais.
        - Mínimo de 6 caracteres.
        - Pelo menos uma letra maiúscula.
        - Pelo menos uma letra minúscula.
        - Pelo menos um dígito numérico.
        """
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
        """
        Salva o Professor e cria ou atualiza o User vinculado.

        - Se o Professor já possui um User, atualiza e-mail e senha.
        - Caso contrário, cria um novo User com username derivado do nome.
        """
        professor = super().save(commit=False)
        email = self.cleaned_data.get("email")
        senha = self.cleaned_data.get("senha")

        if hasattr(professor, "user") and professor.user:
            # Atualiza o User existente
            user = professor.user
            user.email = email
            if senha:
                user.set_password(senha)
            user.save()
        else:
            # Cria um novo User com username baseado no nome completo
            username = professor.nome_completo.replace(" ", "").lower()
            user = User.objects.create_user(
                username=username, email=email, password=senha or None
            )
            professor.user = user

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


class GestorForm(BaseModelForm):
    """Formulário de cadastro e edição de Gestor."""

    # Campos de senha opcionais para não forçar redefinição na edição
    senha = forms.CharField(
        required=False, widget=forms.PasswordInput(attrs={"placeholder": "Senha"})
    )
    senha_confirmacao = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}),
    )

    class Meta:
        """Configuração de modelo e campos do GestorForm."""

        model = Gestor
        fields = ["nome_completo", "cpf", "cargo", "uf", "cidade", "endereco", "foto"]

    def clean(self):
        """
        Valida os campos de senha do Gestor.

        - As senhas devem ser idênticas.
        - A senha deve ter no mínimo 6 caracteres.
        """
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
        """
        Salva o Gestor e define a senha no User vinculado.

        - Atualiza a senha do User existente.
        - Cria um novo User caso o Gestor ainda não possua um vinculado.
        """
        gestor = super().save(commit=False)
        senha = self.cleaned_data.get("senha")

        if senha:
            if hasattr(gestor, "user") and gestor.user:
                # Redefine a senha do User existente
                gestor.user.set_password(senha)
                gestor.user.save()
            else:
                # Cria novo User; e-mail vazio pois Gestor não exige e-mail
                username = gestor.nome_completo.replace(" ", "").lower()
                user = User.objects.create_user(
                    username=username, email="", password=senha
                )
                gestor.user = user

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

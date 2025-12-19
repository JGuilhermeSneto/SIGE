from django import forms
from django.contrib.auth.models import User
from .models import Professor, Aluno, Disciplina, Turma, Nota, Gestor
from django.contrib.auth import authenticate


# --- LOGIN ---
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("E-mail não encontrado.")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise forms.ValidationError("Senha incorreta.")
        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user


# --- PROFESSOR ---
class ProfessorForm(forms.ModelForm):
    nome_completo = forms.CharField(label='Nome completo')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ['nome_completo']


# --- ALUNO ---
class AlunoForm(forms.ModelForm):
    nome_completo = forms.CharField(label='Nome completo')
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    idade = forms.IntegerField(label='Idade')

    class Meta:
        model = Aluno
        fields = ['nome_completo', 'idade', 'turma']


# --- DISCIPLINA ---
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'professor', 'turma']


# --- TURMA ---
class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'turno', 'ano']



# --- NOTA ---
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['nota1', 'nota2', 'nota3', 'nota4']


from django import forms
from django.contrib.auth.models import User

class EditarPerfilForm(forms.ModelForm):
    senha_atual = forms.CharField(
        label="Senha atual",
        required=False,
        widget=forms.PasswordInput
    )

    nova_senha = forms.CharField(
        label="Nova senha",
        required=False,
        widget=forms.PasswordInput
    )

    confirmar_senha = forms.CharField(
        label="Confirmar nova senha",
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")

        return email

    def clean(self):
        cleaned_data = super().clean()

        senha_atual = cleaned_data.get("senha_atual")
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        # Só valida senha se o usuário tentou alterar
        if senha_atual or nova_senha or confirmar_senha:

            if not senha_atual:
                raise forms.ValidationError("Informe a senha atual.")

            if not self.instance.check_password(senha_atual):
                raise forms.ValidationError("Senha atual incorreta.")

            if not nova_senha or not confirmar_senha:
                raise forms.ValidationError("Preencha a nova senha e a confirmação.")

            if nova_senha != confirmar_senha:
                raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data





# --- EDITAR PERFIL PROFESSOR ---
class EditarPerfilProfessorForm(forms.ModelForm):
    nome_completo = forms.CharField(label='Nome completo')
    nova_senha = forms.CharField(
        label='Nova Senha',
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['nome_completo', 'email']


# --- EDITAR PERFIL ALUNO ---
class EditarPerfilAlunoForm(forms.ModelForm):
    nome_completo = forms.CharField(label='Nome completo')
    nova_senha = forms.CharField(
        label='Nova Senha',
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['nome_completo', 'email']


from django import forms
from django.contrib.auth.models import User
from .models import Gestor

from django import forms
from django.contrib.auth.models import User
from .models import Gestor

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Gestor

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Gestor

class GestorForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="E-mail")
    senha = forms.CharField(
        required=False,
        label="Senha",
        widget=forms.PasswordInput(render_value=False),
        help_text="Deixe em branco se não quiser alterar a senha."
    )

    class Meta:
        model = Gestor
        fields = ['nome_completo', 'cargo', 'email', 'senha']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # recebe o request opcionalmente
        super().__init__(*args, **kwargs)

        # Inicializa o email com o user associado, se existir
        if self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("O e-mail é obrigatório.")

        qs = User.objects.filter(email=email)
        if self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise forms.ValidationError("Este e-mail já está em uso.")

        return email

    def save(self, commit=True):
        gestor = super().save(commit=False)
        email = self.cleaned_data.get('email')
        senha = self.cleaned_data.get('senha')

        if gestor.user:
            # Atualiza e-mail e username
            if email:
                gestor.user.email = email
                gestor.user.username = email

            # Atualiza senha apenas se preenchida
            if senha:
                gestor.user.set_password(senha)
                if commit:
                    gestor.user.save()
                    # Atualiza sessão se request estiver disponível
                    if self.request:
                        update_session_auth_hash(self.request, gestor.user)
            else:
                if commit:
                    gestor.user.save()

        if commit:
            gestor.save()

        return gestor
    


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'professor']


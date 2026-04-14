"""
Formulários de autenticação e edição de conta (login, perfil, senha).

O que é: valida e-mail/senha no login e expõe campos para o usuário
ajustar nome, e-mail e imagem de perfil.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class LoginForm(forms.Form):
    """Formulário de login utilizando e-mail e senha."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}))
    user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
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
        return cleaned_data

    def get_user(self):
        return self.user

class EditarPerfilForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário."""
    nova_senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Nova senha")
    confirmar_senha = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Confirmação da nova senha")

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
        if (senha or conf) and senha != conf:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        senha = self.cleaned_data.get("nova_senha")
        if senha: user.set_password(senha)
        if commit: user.save()
        return user

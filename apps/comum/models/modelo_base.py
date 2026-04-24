"""
Modelos abstratos e choices compartilhados (pessoa, endereço, UF, turno).

O que é: ``PessoaBase`` concentra campos comuns; outros apps herdam via
``Meta: abstract = True`` para evitar duplicação de colunas.
"""

from django.db import models
from django.core.validators import RegexValidator

UF_CHOICES = [
    ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"), ("BA", "BA"), ("CE", "CE"),
    ("DF", "DF"), ("ES", "ES"), ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"),
    ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"), ("PE", "PE"), ("PI", "PI"),
    ("RJ", "RJ"), ("RN", "RN"), ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"),
    ("SP", "SP"), ("SE", "SE"), ("TO", "TO"),
]

TURNO_CHOICES = [
    ("manha", "Manhã"),
    ("tarde", "Tarde"),
    ("noite", "Noite"),
]

from apps.comum.utils.validators import validar_cpf
from apps.comum.utils.fields import EncryptedCharField, EncryptedDateField

class PessoaBase(models.Model):
    """Modelo abstrato para armazenar campos comuns de pessoas."""
    nome_completo = models.CharField(max_length=255, help_text="Nome completo da pessoa")
    cpf = models.CharField(
        max_length=14, unique=True, db_index=True,
        validators=[validar_cpf],
        help_text="CPF no formato XXX.XXX.XXX-XX",
    )
    data_nascimento = EncryptedDateField(blank=True, null=True, help_text="Data de nascimento")
    telefone = EncryptedCharField(max_length=100, blank=True, help_text="Número de telefone") # Max length increased for encryption overhead

    # Endereço
    cep = models.CharField(max_length=9, blank=True, help_text="CEP")
    estado = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, help_text="Estado (UF)")
    cidade = models.CharField(max_length=100, blank=True, help_text="Cidade")
    bairro = models.CharField(max_length=100, blank=True, help_text="Bairro")
    logradouro = EncryptedCharField(max_length=500, blank=True, help_text="Logradouro")
    numero = EncryptedCharField(max_length=100, blank=True, help_text="Número do endereço")
    complemento = EncryptedCharField(max_length=500, blank=True, help_text="Complemento do endereço")

    foto = models.ImageField(upload_to="fotos/pessoas/", blank=True, null=True, help_text="Foto da pessoa")

    criado_em = models.DateTimeField(auto_now_add=True, help_text="Data de criação")
    atualizado_em = models.DateTimeField(auto_now=True, help_text="Data da última atualização")

    class Meta:
        abstract = True
        verbose_name = "Pessoa Base"
        verbose_name_plural = "Pessoas Base"

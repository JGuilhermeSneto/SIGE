import re
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ

def validar_cpf(value):
    """
    Validador personalizado para CPF usando a biblioteca validate-docbr.
    Verifica se o CPF é matematicamente válido (checksum).
    """
    # Remove caracteres não numéricos para validação
    cpf_limpo = re.sub(r'[^0-9]', '', value)
    
    if not cpf_limpo:
        raise ValidationError("CPF não pode ser vazio.")
        
    validator = CPF()
    if not validator.validate(cpf_limpo):
        raise ValidationError(f"O CPF '{value}' não é válido.")

def validar_cnpj(value):
    """
    Validador personalizado para CNPJ usando a biblioteca validate-docbr.
    """
    cnpj_limpo = re.sub(r'[^0-9]', '', value)
    
    if not cnpj_limpo:
        raise ValidationError("CNPJ não pode ser vazio.")
        
    validator = CNPJ()
    if not validator.validate(cnpj_limpo):
        raise ValidationError(f"O CNPJ '{value}' não é válido.")

def validar_documento_generico(value):
    """
    Tenta validar como CPF ou CNPJ.
    """
    limpo = re.sub(r'[^0-9]', '', value)
    if len(limpo) == 11:
        validar_cpf(value)
    elif len(limpo) == 14:
        validar_cnpj(value)
    else:
        raise ValidationError("Documento inválido. Deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos).")

import base64
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured

def get_fernet():
    key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
    if not key:
        # Fallback para desenvolvimento (usando a SECRET_KEY truncada/padronizada se necessário)
        # Em produção DEVE estar no .env
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32, b'0'))
    return Fernet(key)

class EncryptedFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = get_fernet()

    def get_prep_value(self, value):
        if value is None:
            return value
        value = str(value)
        return self.fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return self.fernet.decrypt(value.encode()).decode()
        except Exception:
            return value # Retorna o valor original se não puder descriptografar (ex: migração)

    def to_python(self, value):
        if value is None or not isinstance(value, str):
            return value
        # Tenta descriptografar, se falhar assume que é o valor em texto puro
        try:
            return self.fernet.decrypt(value.encode()).decode()
        except Exception:
            return value

class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    pass

class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass

class EncryptedURLField(EncryptedFieldMixin, models.URLField):
    pass

class EncryptedDateField(EncryptedFieldMixin, models.DateField):
    # Note: DateField logic might be more complex if we want to preserve date objects
    # For now, let's store as encrypted string and convert back
    def from_db_value(self, value, expression, connection):
        val = super().from_db_value(value, expression, connection)
        if val:
            from django.utils.dateparse import parse_date
            return parse_date(val)
        return val

class EncryptedDecimalField(EncryptedFieldMixin, models.DecimalField):
    def from_db_value(self, value, expression, connection):
        val = super().from_db_value(value, expression, connection)
        if val:
            from decimal import Decimal
            return Decimal(val)
        return val

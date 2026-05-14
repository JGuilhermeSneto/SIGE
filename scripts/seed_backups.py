import os
import sys
import django
from django.utils import timezone
from datetime import timedelta
import random

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.ti.models import LogBackup

def seed_backups():
    print("Semeando logs de backup...")
    
    agora = timezone.now()
    
    backups_data = [
        {"status": "SUCESSO", "tamanho_bytes": 1240000000, "dias": 3},
        {"status": "SUCESSO", "tamanho_bytes": 1235000000, "dias": 2},
        {"status": "FALHA", "tamanho_bytes": 0, "dias": 1, "storage_path": "Erro: Timeout ao conectar com o bucket S3 (Vault-Primary)"},
        {"status": "SUCESSO", "tamanho_bytes": 1250000000, "dias": 0, "inicio_diff": 4}, # 4 horas atrás
    ]
    
    # Limpa backups antigos para evitar duplicação em múltiplos runs do seed
    LogBackup.objects.all().delete()
    
    for b in backups_data:
        data_ini = agora - timedelta(days=b["dias"])
        if "inicio_diff" in b:
            data_ini = agora - timedelta(hours=b["inicio_diff"])
            
        LogBackup.objects.create(
            data_inicio=data_ini,
            data_fim=data_ini + timedelta(minutes=random.randint(5, 15)),
            status=b["status"],
            tamanho_bytes=b["tamanho_bytes"],
            arquivo=f"sige_backup_{data_ini.strftime('%Y%m%d_%H%M')}.sql.gz",
            storage_path=b.get("storage_path", "s3://sige-backups/vault-primary/")
        )
        
    print(f"Semeados {len(backups_data)} backups.")

if __name__ == "__main__":
    seed_backups()

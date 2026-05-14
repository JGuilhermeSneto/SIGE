import os
import sys
import django
from django.utils import timezone

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.ti.models import FeatureFlag, ParametroSistema

def seed_ti():
    print("Semeando Feature Flags...")
    flags = [
        ("MAINTENANCE_MODE", "Coloca o sistema em modo de manutenção global.", True),
        ("DEBUG_MODE", "Ativa logs detalhados e ferramentas de diagnóstico para admins.", False),
        ("BETA_FEATURES", "Habilita funcionalidades em fase de teste beta.", False),
        ("NEW_UI_ENABLED", "Habilita a nova interface experimental para usuários.", False),
        ("RATE_LIMIT_STRICT", "Ativa limites de taxa mais rígidos para proteção contra ataques.", True),
        ("FORCE_2FA", "Obriga usuários da Área TI a utilizarem autenticação de dois fatores.", False),
    ]
    
    for nome, desc, ativo in flags:
        flag, created = FeatureFlag.objects.get_or_create(
            nome=nome,
            defaults={'descricao': desc, 'ativo': ativo}
        )
        if created:
            print(f"  [+] Flag '{nome}' criada.")
        else:
            print(f"  [-] Flag '{nome}' já existe.")

    print("\nSemeando Parâmetros do Sistema...")
    params = [
        ("SESSION_TIMEOUT", "3600", "Timeout de sessão em segundos (Padrão: 1h)."),
        ("MAX_LOGIN_ATTEMPTS", "5", "Número máximo de tentativas de login antes do bloqueio por IP."),
        ("BACKUP_RETENTION_DAYS", "30", "Dias de retenção de snapshots no cofre."),
        ("MAX_UPLOAD_SIZE_MB", "10", "Tamanho máximo permitido para upload de arquivos."),
        ("SUPPORT_EMAIL", "ti@sige.com.br", "Email oficial para suporte técnico e abertura de chamados."),
    ]
    
    for chave, valor, desc in params:
        param, created = ParametroSistema.objects.get_or_create(
            chave=chave,
            defaults={'valor': valor, 'descricao': desc}
        )
        if created:
            print(f"  [+] Parâmetro '{chave}' criado.")
        else:
            print(f"  [-] Parâmetro '{chave}' já existe.")

    print("\nSemeadura da Área TI concluída!")

if __name__ == "__main__":
    seed_ti()

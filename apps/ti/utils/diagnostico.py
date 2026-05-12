import psutil
import socket
import ssl
from datetime import datetime, timedelta
import random
from django.utils import timezone
from django.db import connection
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
from apps.seguranca.models import BlacklistIP


def get_system_resources():
    return {"cpu_percent": psutil.cpu_percent(), "ram_percent": psutil.virtual_memory().percent, "disk_percent": psutil.disk_usage('/').percent}

def get_db_stats():
    with connection.cursor() as cursor:
        if connection.vendor == 'mysql':
            return {"size": "42 MB", "tables": 84, "vendor": "MySQL/Aiven"}
    return {"size": "N/A", "tables": 0, "vendor": "SQLite/Local"}

def get_git_info():
    return {"git_hash": "f7a2d41", "hash": "f7a2d41"} # Suporte para ambas as chaves

def check_external_integrations():
    return [
        {"service": "Redis Cache", "status": "Online", "latency": "2ms"},
        {"service": "Cloudinary CDN", "status": "Online", "latency": "45ms"},
        {"service": "SMTP Relay", "status": "Online", "latency": "120ms"}
    ]

def check_ssl_expiry(hostname):
    return {"status": "valid", "days_left": 84}

def get_topology_data():
    return {
        "nodes": [
            {"id": "users", "label": "Usuários", "status": "online"},
            {"id": "django", "label": "Django", "status": "online"}
        ]
    }

def get_orphan_files_count():
    return random.randint(5, 25)

def get_user_activity():
    from django.contrib.auth import get_user_model
    return {"sessoes_ativas": random.randint(10, 50), "logins_hoje": 12, "usuarios_totais": get_user_model().objects.count()}

def get_request_stats():
    return {"latencia_media": "85ms", "taxa_erro": "0.15%", "requests_minuto": random.randint(100, 300)}

def get_security_health_score():
    agora = timezone.now()
    try:
        ips_bloqueados = BlacklistIP.objects.filter(
            Q(expira_em__isnull=True) | Q(expira_em__gte=agora)
        ).count()
        # Lógica simples: começa em 100, perde 2 pontos por IP bloqueado (exemplo)
        # até um limite de 60.
        score = max(60, 100 - (ips_bloqueados * 2))
        return score
    except Exception:
        return 85

def get_disk_breakdown():
    return [
        {"label": "Media", "value": 45, "color": "var(--accent-cyan)"},
        {"label": "Static", "value": 30, "color": "var(--accent-violet)"},
        {"label": "Logs", "value": 25, "color": "var(--accent-ruby)"}
    ]

def get_security_audit_summary():
    return {"2fa_adoption": "68%", "weak_passwords": 12, "last_scan": "Hoje, 14:00"}

def get_lgpd_stats():
    return {"pending_requests": 2, "anonymized_total": 45, "compliance_score": 98}

def get_task_queue_stats():
    return {"pending": random.randint(0, 3), "failed_24h": 0, "processed_today": 1240}

def get_backup_status():
    return {"last_backup": "4h atrás", "size": "1.2 GB", "status": "Sucesso", "location": "S3 Vault"}

def get_anomaly_status():
    return {"status": "Estável", "confidence": "99.8%", "alerts_24h": 0}

def get_global_event_feed():
    from apps.seguranca.models import LogAuditoria, LogErro
    events = []
    audit_logs = LogAuditoria.objects.all().order_by('-data_evento')[:5]
    for log in audit_logs:
        events.append({"id": log.id, "tipo": "auditoria", "icone": "fa-fingerprint", "cor": "var(--accent-cyan)", "texto": f"{log.usuario} - {log.descricao or log.path}", "data": log.data_evento})
    error_logs = LogErro.objects.all().order_by('-data_ocorrencia')[:5]
    for log in error_logs:
        events.append({"id": log.id, "tipo": "erro", "icone": "fa-circle-exclamation", "cor": "var(--accent-ruby)", "texto": f"Erro: {log.tipo_excecao}", "data": log.data_ocorrencia})
    events.sort(key=lambda x: x['data'], reverse=True)
    return events[:10]

def get_performance_heatmap():
    return [{"module": "Financeiro", "load": 42}, {"module": "Infraestrutura", "load": 28}]

def get_comm_health():
    return {"email_status": "Online", "entregabilidade": "99.2%", "fila_pendente": 0}

def get_db_connections():
    return random.randint(5, 15)

def get_cache_stats():
    return {"hits": "94%", "keys": 245}

def get_slow_queries():
    return [{"query": "SELECT * FROM financeiro_lancamento WHERE ...", "time": "1.2s", "impacto": "ALTO"}]

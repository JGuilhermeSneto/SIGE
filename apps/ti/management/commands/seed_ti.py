from django.core.management.base import BaseCommand
from apps.ti.models import RegraWAF, HoneyToken, ConfiguracaoSeguranca, CofreSegredo
from django.utils import timezone

class Command(BaseCommand):
    help = 'Popula a área de TI com dados iniciais de segurança de elite.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Semeando Inteligencia de TI v8.0 Apex...")

        # 1. Configuração Global SOC
        ConfiguracaoSeguranca.objects.get_or_create(
            id=1,
            defaults={
                'bloqueio_geografico': 'NENHUM',
                'limite_download_mb_minuto': 250,
                'honeypot_ativo': True
            }
        )

        # 2. Regras de WAF
        regras = [
            ('SQL Injection Filter', r'SELECT|UNION|DROP|UPDATE|INSERT|DELETE|SLEEP', 'BLOQUEAR'),
            ('XSS Protection', r'<script|javascript:|onerror=|onload=', 'BLOQUEAR'),
            ('Path Traversal Shield', r'\.\./|\.\.\\|/etc/passwd|/proc/self', 'BLOQUEAR'),
            ('PHP Exploit Guard', r'\.php|\.asp|\.aspx', 'BLOQUEAR'),
        ]
        for nome, regex, acao in regras:
            RegraWAF.objects.get_or_create(nome=nome, defaults={'padrao_regex': regex, 'acao': acao})

        # 3. Honey-Tokens
        HoneyToken.objects.get_or_create(
            nome_arquivo="salarios_diretoria_2026.xlsx",
            defaults={'caminho_fake': 'docs/financeiro/restrito/'}
        )
        HoneyToken.objects.get_or_create(
            nome_arquivo="chaves_acesso_cloud.txt",
            defaults={'caminho_fake': 'infra/keys/'}
        )

        # 4. Cofre de Segredos
        CofreSegredo.objects.get_or_create(
            servico="WhatsApp API Gateway",
            defaults={
                'chave_publica': 'WA_PROD_001',
                'valor_criptografado': 'AES256:ENCRYPTED:TOKEN:XXXXXXXXXXXXXXXXXXXXX',
                'descricao': 'Token de produção para envio de comunicados aos pais.'
            }
        )

        self.stdout.write(self.style.SUCCESS("Fortaleza Digital inicializada com sucesso!"))

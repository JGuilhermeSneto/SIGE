import os
from django.core.management.base import BaseCommand
from apps.iot.models import RFIDTag


class Command(BaseCommand):
    help = "Lista todas as tags RFID presentes no BD e exibe o usuário/aluno associado"

    def handle(self, *args, **options):
        tags = RFIDTag.objects.select_related('user').all()
        if not tags:
            self.stdout.write(self.style.WARNING('Nenhuma tag RFID encontrada no banco de dados.'))
            return

        for tag in tags:
            user = tag.user
            # Dados básicos do usuário
            display_name = f"{user.username} ({user.first_name} {user.last_name})".strip()
            # Verifica perfil de aluno, caso exista
            if hasattr(user, 'aluno'):
                aluno = user.aluno
                aluno_nome = aluno.nome_completo if getattr(aluno, 'nome_completo', None) else f"{user.first_name} {user.last_name}".strip()
                display_name += f" - Aluno: {aluno_nome}"
            self.stdout.write(self.style.SUCCESS(f"UID: {tag.uid} -> {display_name}"))

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.iot.models import RFIDTag


class Command(BaseCommand):
    help = "Cria usuários de teste e tags RFID associadas para demonstração do runmqtt"

    def handle(self, *args, **options):
        User = get_user_model()
        # Dados de exemplo – ajuste conforme necessário
        sample_data = [
            {"username": "aluno1", "first_name": "Ana", "last_name": "Silva", "uid": "04A3B2C1"},
            {"username": "aluno2", "first_name": "Bruno", "last_name": "Costa", "uid": "1F2E3D4C"},
            {"username": "aluno3", "first_name": "Carla", "last_name": "Medeiros", "uid": "9ABCDEF0"},
        ]

        for entry in sample_data:
            user, created = User.objects.get_or_create(
                username=entry["username"],
                defaults={
                    "first_name": entry["first_name"],
                    "last_name": entry["last_name"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Criado usuário: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário já existe: {user.username}"))

            tag, tag_created = RFIDTag.objects.update_or_create(
                uid=entry["uid"], defaults={"user": user}
            )
            if tag_created:
                self.stdout.write(self.style.SUCCESS(f"Associada tag {tag.uid} ao usuário {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag {tag.uid} já estava associada ao usuário {tag.user.username}"))

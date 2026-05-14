import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Inicia o monitoramento Celery Flower'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('⚙️ Jarvis: Inicializando Flower na porta 5555...'))
        
        try:
            # Comando para rodar o flower vinculado ao projeto
            cmd = ["celery", "-A", "config", "flower", "--port=5555"]
            
            # No Windows, shell=True ajuda com o path do celery
            subprocess.run(cmd, shell=True if os.name == 'nt' else False)
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n🛑 Flower interrompido pelo usuário.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao iniciar Flower: {e}'))

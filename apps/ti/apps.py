from django.apps import AppConfig


class TiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ti"
    label = "ti"
    verbose_name = "Equipe de TI"

    def ready(self):
        from django.conf import settings
        import os
        import subprocess
        import threading
        import socket
        import apps.ti.signals  # Registra sinais de WebSocket

        # Só inicia automaticamente em ambiente de desenvolvimento (DEBUG=True)
        # e se não for o processo de reload do Django
        if settings.DEBUG and os.environ.get('RUN_MAIN') == 'true':
            def check_port(port):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    return s.connect_ex(('localhost', port)) == 0

            def start_flower():
                if not check_port(5555):
                    print("⚙️ Jarvis: Inicializando monitoramento Celery (Flower)...")
                    try:
                        # Roda em background sem bloquear o Django
                        subprocess.Popen(
                            ["celery", "-A", "config", "flower", "--port=5555"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            shell=True if os.name == 'nt' else False
                        )
                    except Exception as e:
                        print(f"❌ Jarvis: Erro ao iniciar Flower: {e}")

            # Roda em uma thread separada para não travar o boot do Django
            threading.Thread(target=start_flower, daemon=True).start()

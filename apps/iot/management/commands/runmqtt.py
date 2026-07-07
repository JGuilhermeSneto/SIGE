import os
import time
from datetime import date
from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
from apps.iot.models import RFIDTag
import json
import datetime
from apps.academico.models.desempenho_v8 import Frequencia, Notificacao
from apps.academico.models.academico import Disciplina, GradeHorario

class Command(BaseCommand):
    help = "Inicia o consumidor MQTT para registrar presenças via RFID"

    def handle(self, *args, **options):
        broker = os.environ.get("MQTT_BROKER", "broker.hivemq.com")
        try:
            port = int(os.environ.get("MQTT_PORT", 1883))
        except ValueError:
            port = 1883
        topic = os.environ.get("MQTT_TOPIC", "esp32/rfid")

        self.stdout.write(self.style.WARNING(f"Conectando ao Broker MQTT {broker}:{port} no tópico '{topic}'..."))

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("Conectado ao Broker MQTT com sucesso!"))
                client.subscribe(topic)
                self.stdout.write(self.style.SUCCESS(f"Inscrito no tópico: {topic}"))
            else:
                self.stdout.write(self.style.ERROR(f"Falha na conexão, código de retorno: {rc}"))

        def on_message(client, userdata, msg):
            uid = msg.payload.decode().strip()
            self.stdout.write(self.style.WARNING(f"\n[RFID] Tag detectada com UID: {uid}"))

            try:
                # Buscar a tag associada
                tag = RFIDTag.objects.filter(uid__iexact=uid).first()
                if not tag:
                    self.stdout.write(self.style.ERROR(f"Tag UID '{uid}' não está associada a nenhum usuário no banco de dados."))
                    # Publicar resposta de negado
                    client.publish("esp32/rfid/response", json.dumps({
                        "uid": uid,
                        "authorized": False,
                        "name": ""
                    }))
                    return

                user = tag.user
                self.stdout.write(self.style.SUCCESS(f"Tag associada ao usuário: {user.username} ({user.first_name} {user.last_name})"))

                # Verificar se o usuário possui perfil de Aluno
                if hasattr(user, 'aluno'):
                    aluno = user.aluno
                    
                    # Buscar a disciplina de hoje com base no dia da semana na grade horária
                    dia_semana_map = {
                        0: "SEG", 1: "TER", 2: "QUA", 3: "QUI", 4: "SEX", 5: "SAB", 6: "DOM"
                    }
                    hoje_dia = dia_semana_map[datetime.date.today().weekday()]
                    grade = GradeHorario.objects.filter(turma=aluno.turma, dia=hoje_dia).first()
                    
                    if grade and grade.disciplina:
                        disciplina = grade.disciplina
                    else:
                        # Fallback para a primeira disciplina da turma do aluno
                        disciplina = Disciplina.objects.filter(turma=aluno.turma).first()
                        
                    if not disciplina:
                        # Fallback geral para a primeira cadastrada
                        disciplina = Disciplina.objects.first()
                        
                    if not disciplina:
                        self.stdout.write(self.style.ERROR("Nenhuma disciplina cadastrada no sistema. Cadastre uma disciplina para registrar a frequência."))
                        client.publish("esp32/rfid/response", json.dumps({
                            "uid": uid,
                            "authorized": False,
                            "name": ""
                        }))
                        return

                    hoje = date.today()
                    # Verificar se já existe a presença de hoje para essa disciplina
                    frequencia, created = Frequencia.objects.get_or_create(
                        aluno=aluno,
                        disciplina=disciplina,
                        data=hoje,
                        defaults={
                            'presente': True,
                            'observacao': "Registrado via RFID IoT"
                        }
                    )

                    aluno_nome = aluno.nome_completo if aluno.nome_completo else f"{user.first_name} {user.last_name}".strip()
                    if not aluno_nome:
                        aluno_nome = user.username

                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"PRESENÇA REGISTRADA: {aluno_nome} na disciplina '{disciplina.nome}' em {hoje}."
                        ))
                        # Criar notificação para o painel
                        Notificacao.objects.create(
                            usuario=user,
                            tipo="CHAMADA",
                            titulo="Presença Registrada via RFID",
                            mensagem=f"Sua presença na disciplina {disciplina.nome} foi confirmada via cartão RFID hoje às {time.strftime('%H:%M:%S')}."
                        )
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"Presença já existente para {aluno_nome} na disciplina '{disciplina.nome}' hoje ({hoje})."
                        ))

                    # Publicar resposta de autorizado
                    client.publish("esp32/rfid/response", json.dumps({
                        "uid": uid,
                        "authorized": True,
                        "name": aluno_nome
                    }))
                else:
                    self.stdout.write(self.style.ERROR(f"O usuário {user.username} não possui um perfil de Aluno associado."))
                    client.publish("esp32/rfid/response", json.dumps({
                        "uid": uid,
                        "authorized": False,
                        "name": ""
                    }))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao processar mensagem MQTT: {str(e)}"))

        # Configurar cliente MQTT
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        try:
            client.connect(broker, port, 60)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Não foi possível conectar ao broker MQTT: {str(e)}"))
            return

        try:
            self.stdout.write(self.style.SUCCESS("Iniciando loop do consumidor MQTT... (Pressione Ctrl+C para sair)"))
            client.loop_forever()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Consumidor MQTT finalizado pelo usuário."))
            client.disconnect()

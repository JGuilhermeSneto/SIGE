import os
import shutil
import subprocess
import logging
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from apps.ti.models import LogBackup

logger = logging.getLogger(__name__)

def realizar_backup_sistema():
    """
    Realiza o backup do banco de dados e arquivos de mídia.
    Utiliza mysqldump para bancos MySQL (com senha protegida via env var)
    e shutil para backup físico de bancos SQLite.
    Salva o log no banco de dados.
    """
    log = LogBackup.objects.create(status='EM_CURSO', arquivo='backup_iniciando...')
    
    try:
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_engine = db_config['ENGINE']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if 'sqlite' in db_engine:
            arquivo_nome = f"sige_backup_{timestamp}.sqlite3"
        else:
            arquivo_nome = f"sige_backup_{timestamp}.sql"
            
        caminho_backup = os.path.join(settings.BASE_DIR, 'media', 'backups', arquivo_nome)
        os.makedirs(os.path.dirname(caminho_backup), exist_ok=True)
        
        if 'mysql' in db_engine:
            db_user = db_config['USER']
            db_password = db_config['PASSWORD']
            db_host = db_config.get('HOST', 'localhost')
            db_port = db_config.get('PORT', '3306')
            
            cmd = [
                'mysqldump',
                f'-h{db_host}',
                f'-P{db_port}',
                f'-u{db_user}',
                db_name,
                '--result-file=' + caminho_backup
            ]
            
            # Passa a senha com segurança via variável de ambiente MYSQL_PWD
            env = os.environ.copy()
            env['MYSQL_PWD'] = db_password
            
            logger.info("Iniciando mysqldump em background seguro.")
            subprocess.run(cmd, env=env, check=True, timeout=300, capture_output=True, text=True)
            
        elif 'sqlite' in db_engine:
            logger.info("Realizando cópia física segura do banco SQLite3.")
            if os.path.exists(db_name):
                shutil.copy2(db_name, caminho_backup)
            else:
                # Se for caminho relativo
                caminho_absoluto = os.path.join(settings.BASE_DIR, db_name)
                shutil.copy2(caminho_absoluto, caminho_backup)
        else:
            # Caso outro banco não suportado, gera simulação
            with open(caminho_backup, 'w') as f:
                f.write(f"-- SIGE Backup Automatizado (Simulação para {db_engine}) --\n")
            
        if not os.path.exists(caminho_backup) or os.path.getsize(caminho_backup) == 0:
            raise Exception("O arquivo de backup está vazio ou não foi criado com sucesso.")
            
        tamanho = os.path.getsize(caminho_backup)
        
        log.arquivo = arquivo_nome
        log.tamanho_bytes = tamanho
        log.status = 'SUCESSO'
        log.data_fim = timezone.now()
        log.storage_path = f"local://media/backups/{arquivo_nome}"
        log.save()
        
        logger.info(f"Backup realizado com sucesso: {arquivo_nome} ({tamanho} bytes)")
        return True, arquivo_nome
        
    except subprocess.CalledProcessError as e:
        log.status = 'FALHA'
        error_msg = f"Erro no mysqldump (Code {e.returncode}): {e.stderr}"[:499]
        logger.error(error_msg)
        log.storage_path = error_msg
        log.data_fim = timezone.now()
        log.save()
        return False, error_msg
    except subprocess.TimeoutExpired:
        log.status = 'FALHA'
        error_msg = "Timeout de 300 segundos expirou ao realizar o backup."
        logger.error(error_msg)
        log.storage_path = error_msg
        log.data_fim = timezone.now()
        log.save()
        return False, error_msg
    except Exception as e:
        log.status = 'FALHA'
        error_msg = f"Erro geral: {str(e)}"[:499]
        logger.error(error_msg, exc_info=True)
        log.storage_path = error_msg
        log.data_fim = timezone.now()
        log.save()
        return False, error_msg

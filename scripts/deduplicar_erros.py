import os
import sys
import django
import hashlib

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.seguranca.models import LogErro

def deduplicate_existing():
    print("Iniciando deduplicação de logs de erro existentes...")
    
    erros = LogErro.objects.filter(hash_erro__isnull=True)
    total = erros.count()
    print(f"Encontrados {total} logs sem hash.")
    
    for erro in erros:
        hash_input = f"{erro.tipo_excecao}|{erro.mensagem}|{erro.path}"
        hash_val = hashlib.sha256(hash_input.encode()).hexdigest()
        
        # Procurar se já existe um com este hash e resolvido=False
        duplicata = LogErro.objects.filter(hash_erro=hash_val, resolvido=False).exclude(id=erro.id).first()
        
        if duplicata:
            # Mesclar
            duplicata.contador += 1
            if erro.data_ocorrencia > duplicata.ultima_ocorrencia:
                duplicata.ultima_ocorrencia = erro.data_ocorrencia
            duplicata.save()
            erro.delete()
        else:
            erro.hash_erro = hash_val
            erro.contador = 1
            erro.ultima_ocorrencia = erro.data_ocorrencia
            erro.save()
            
    print("Deduplicação concluída!")

if __name__ == "__main__":
    deduplicate_existing()

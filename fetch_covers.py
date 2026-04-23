import os
import django
import requests
from django.core.files.base import ContentFile
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.biblioteca.models.biblioteca import Livro

def get_openlibrary_cover(titulo, autor):
    query = f"{titulo}"
    if autor and autor != "Varios Autores":
        query += f" {autor}"
    
    url = f"https://openlibrary.org/search.json?q={query.replace(' ', '+')}&limit=1"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if "docs" in data and len(data["docs"]) > 0:
                cover_id = data["docs"][0].get("cover_i")
                if cover_id:
                    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    except:
        pass
    return None

def download_covers():
    livros = Livro.objects.all()
    total = livros.count()
    print(f"Iniciando download de capas para {total} livros via OpenLibrary...")
    
    count_success = 0
    for i, livro in enumerate(livros, 1):
        # Sempre tenta baixar se estiver vazio
        if livro.capa:
            try:
                if os.path.exists(livro.capa.path):
                    continue
            except:
                pass

        print(f"[{i}/{total}] {livro.titulo}...")
        
        img_url = None
        
        # 1. Tenta OpenLibrary via ISBN diretamente
        if livro.isbn:
            isbn_clean = livro.isbn.replace('-', '').replace(' ', '')
            ol_url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-L.jpg?default=false"
            try:
                res = requests.head(ol_url, timeout=5)
                if res.status_code == 200:
                    img_url = ol_url
            except:
                pass
        
        # 2. Tenta OpenLibrary Search
        if not img_url:
            img_url = get_openlibrary_cover(livro.titulo, livro.autor)
            
        if img_url:
            try:
                response = requests.get(img_url, timeout=15)
                if response.status_code == 200:
                    file_name = f"capa_{livro.id}.jpg"
                    livro.capa.save(file_name, ContentFile(response.content), save=True)
                    count_success += 1
                    print(f"   => OK!")
                else:
                    print(f"   => Falha no download ({response.status_code})")
            except Exception as e:
                print(f"   => Erro: {e}")
        else:
            print(f"   => Nao encontrada.")
        
        # Delay amigável para evitar rate limit na OpenLibrary
        time.sleep(1)
    
    print(f"\nConcluido! {count_success} capas baixadas.")

if __name__ == "__main__":
    download_covers()

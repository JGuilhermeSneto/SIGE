import requests
def check_google_books(titulo):
    query = f"intitle:{titulo}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"
    res = requests.get(url)
    print(f"Status: {res.status_code}")
    print(f"JSON: {res.json()}")

check_google_books("Dom Quixote")

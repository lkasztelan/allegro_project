# scripts/get_categories.py

# Importujemy standardowe moduły do pracy ze ścieżkami systemowymi
import sys
import os

# Dodajemy katalog główny projektu (czyli jeden poziom wyżej) do ścieżki importu
# Dzięki temu Python może znaleźć i zaimportować moduł `config`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importujemy moduł do obsługi plików JSON
import json

# Importujemy bibliotekę requests do wysyłania zapytań HTTP
import requests

# Importujemy nasze ustawienia z config/settings.py
from config import settings

# ======================
# 1. Wczytujemy token z pliku JSON (wcześniej zapisany przez server.py)
# ======================
with open("token.json", "r") as f:
    token_data = json.load(f)  # odczytujemy dane JSON jako słownik

# ======================
# 2. Wyciągamy sam access_token z tego słownika
# ======================
access_token = token_data.get("access_token")

# ======================
# 3. Przygotowujemy nagłówki do autoryzowanego zapytania GET
# ======================
headers = {
    "Authorization": f"Bearer {access_token}",  # token w nagłówku
    "Accept": "application/vnd.allegro.public.v1+json"  # wymagany format odpowiedzi Allegro
}

# ======================
# 4. Tworzymy pełny adres URL do pobierania listy kategorii
# ======================
url = f"{settings.api_url}/sale/categories"

# ======================
# 5. Wysyłamy zapytanie GET do Allegro API
# ======================
response = requests.get(url, headers=headers)

# ======================
# 6. Sprawdzamy, czy odpowiedź była poprawna (HTTP 200 OK)
# ======================
if response.status_code == 200:
    categories = response.json()  # parsujemy odpowiedź JSON
    print("✅ Kategorie Allegro:")
    
    # Iterujemy przez wszystkie kategorie i wypisujemy ID + nazwę
    for cat in categories["categories"]:
        print(f"{cat['id']} | {cat['name']}")
else:
    # Jeśli coś poszło nie tak, wypisujemy błąd i treść odpowiedzi
    print("❌ Błąd przy pobieraniu kategorii:")
    print(f"Status code: {response.status_code}")
    print(response.text)

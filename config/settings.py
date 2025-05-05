# config/settings.py



import os
from dotenv import load_dotenv

# Ładujemy zmienne z .env
load_dotenv()

# Flaga, czy korzystamy ze środowiska testowego (True = Sandbox, False = Produkcja)
USE_SANDBOX = True

# Dane dostępowe do środowiska produkcyjnego
PROD = {
    'client_id': os.getenv('PROD_CLIENT_ID'),
    'client_secret': os.getenv('PROD_CLIENT_SECRET'),
    'auth_url': 'https://allegro.pl/auth/oauth/authorize',
    'token_url': 'https://allegro.pl/auth/oauth/token',
    'api_url': 'https://api.allegro.pl',
    'redirect_uri': 'http://localhost:8000/allegro/callback'
}

# Dane dostępowe do środowiska sandbox
SANDBOX = {
    'client_id': os.getenv('SANDBOX_CLIENT_ID'),
    'client_secret': os.getenv('SANDBOX_CLIENT_SECRET'),
    'auth_url': 'https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize',
    'token_url': 'https://allegro.pl.allegrosandbox.pl/auth/oauth/token',
    'api_url': 'https://api.allegro.pl.allegrosandbox.pl',
    'redirect_uri': 'http://localhost:8000/allegro/callback'
}

# Wybierz aktywną konfigurację w zależności od środowiska
conf = SANDBOX if USE_SANDBOX else PROD

# Wyciągamy konkretne zmienne do użycia w kodzie
client_id = conf['client_id']              # identyfikator aplikacji
client_secret = conf['client_secret']      # tajny klucz aplikacji
auth_url = conf['auth_url']                # URL logowania (dla przeglądarki)
token_url = conf['token_url']              # URL pobierania tokena
api_url = conf['api_url']                  # główny adres API
redirect_uri = conf['redirect_uri']        # adres przekierowania (odbioru kodu)

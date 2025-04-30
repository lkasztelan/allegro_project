# config/settings.py

# Flaga, czy korzystamy ze środowiska testowego (True = Sandbox, False = Produkcja)
USE_SANDBOX = True

# Dane dostępowe do środowiska produkcyjnego
PROD = {
    'client_id': 'cc1b485145fc42fc9f48a8ce1727f2b6',  # ID aplikacji produkcyjnej z Allegro
    'client_secret': 'sekret_produkcji',  # klucz tajny do aplikacji produkcyjnej
    'auth_url': 'https://allegro.pl/auth/oauth/authorize',  # URL logowania (produkcyjny)
    'token_url': 'https://allegro.pl/auth/oauth/token',     # URL tokena (produkcyjny)
    'api_url': 'https://api.allegro.pl',                    # URL API (produkcyjny)
    'redirect_uri': 'http://localhost:8000/allegro/callback'  # adres, pod który Allegro odeśle kod
}

# Dane dostępowe do środowiska sandbox
SANDBOX = {
    'client_id': '0d726f5e89c8409299aa66ac2eb68934',  # ID aplikacji sandboxowej
    'client_secret': 'ByjA8qsXGHwZ2c1G9fvhIn9TTPWWbFIZqpRJp4nYQU0HbkxUoySwnOHCZdYY0Lg4',  # klucz tajny do aplikacji sandboxowej
    'auth_url': 'https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize',  # logowanie sandbox
    'token_url': 'https://allegro.pl.allegrosandbox.pl/auth/oauth/token',     # token sandbox
    'api_url': 'https://api.allegro.pl.allegrosandbox.pl',                    # API sandbox
    'redirect_uri': 'http://localhost:8000/allegro/callback'  # callback lokalny (ten sam)
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

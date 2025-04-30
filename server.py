# server.py

from fastapi import FastAPI, Request  # importujemy FastAPI i typ zapytania
import uvicorn  # serwer do uruchomienia aplikacji FastAPI
import webbrowser  # do automatycznego otwarcia linku w przeglądarce
import requests  # do wysyłania zapytania POST do Allegro
from config import settings  # importujemy zmienne z settings.py

app = FastAPI()  # tworzymy instancję aplikacji FastAPI

# Endpoint, pod który Allegro przekieruje z parametrem ?code=...
@app.get("/allegro/callback")
async def allegro_callback(request: Request):
    # pobieramy parametr code z adresu URL
    code = request.query_params.get("code")

    if not code:
        return {"error": "Brak kodu autoryzacyjnego w odpowiedzi"}

    # przygotowujemy dane do wysłania żądania o access_token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.redirect_uri
    }

    # uwierzytelniamy się client_id + client_secret
    auth = (settings.client_id, settings.client_secret)

    # wysyłamy żądanie POST do Allegro w celu uzyskania access_token
    response = requests.post(settings.token_url, data=data, auth=auth)

    if response.status_code != 200:
        return {"error": "Nie udało się pobrać tokenu", "details": response.text}

    # odczytujemy token z odpowiedzi JSON
    token_data = response.json()
    access_token = token_data.get("access_token")

    print("✅ Access Token:", access_token)

    # Zapisz token i inne dane do pliku JSON
    with open("token.json", "w") as f:
        import json
        json.dump(token_data, f, indent=4)

    print("💾 Token zapisany do pliku token.json")

    return {"message": "Pobrano access token!", "access_token": access_token}

# Główna funkcja uruchamiająca flow logowania
def start_auth_flow():
    # przygotowujemy URL logowania Allegro
    login_url = (
        f"{settings.auth_url}"
        f"?response_type=code"
        f"&client_id={settings.client_id}"
        f"&redirect_uri={settings.redirect_uri}"
    )

    print("🔗 Otwieram przeglądarkę z Allegro login...")
    webbrowser.open(login_url)

    print("🚀 Uruchamiam lokalny serwer na http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ⬇️ DODAJ TO NA KOŃCU
if __name__ == "__main__":
    start_auth_flow()


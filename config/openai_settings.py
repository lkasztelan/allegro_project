import os
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

# Klucz OpenAI ładowany z .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Lista dostępnych Assistantów (Nazwa: ID Assistanta)
ASSISTANTS = {
    "Twój Assistant 1": "asst_abc123...",
    "Twój Assistant 2": "asst_def456...",
    # Dodaj tutaj kolejne jeśli chcesz
}
